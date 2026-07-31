import logging
import os

from dotenv import load_dotenv
from flask import Flask
from flask import request as flask_request
from flask_cors import CORS

from database.init_db import apply_schema
from extensions import socketio
from models.profile_model import reset_all_online_status
from routes.auth_routes import auth_routes
from routes.browse_routes import browse_routes
from routes.chat_routes import chat_routes
from routes.profile_routes import profile_routes
from routes.social_routes import social_routes
from services.socket_service import handle_connect, handle_disconnect
from utils.http_errors import register_error_handlers
from utils.logger import configure_logging

load_dotenv()

configure_logging()
logger = logging.getLogger(__name__)

MAX_CONTENT_LENGTH = 5 * 1024 * 1024
DEFAULT_FRONTEND_URL = "http://localhost:5173"


def get_secret_key():
    """Échoue au démarrage plutôt qu'à la première signature de token."""
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        raise RuntimeError("SECRET_KEY is not set: refusing to start")
    return secret_key


def is_debug_enabled():
    return os.getenv("FLASK_DEBUG", "FALSE").upper() in ("1", "TRUE")


frontend_url = os.getenv("FRONTEND_URL", DEFAULT_FRONTEND_URL)

app = Flask(__name__)

CORS(app, supports_credentials=True, origins=[frontend_url])
app.config['SECRET_KEY'] = get_secret_key()
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

register_error_handlers(app)

socketio.init_app(
    app,
    cors_allowed_origins=frontend_url,
    manage_session=False
)

@app.route("/")
def index():
    return "Matcha backend is running"

@socketio.on("connect")
def on_connect():
    handle_connect(socketio, flask_request)

@socketio.on("disconnect")
def on_disconnect():
    handle_disconnect(flask_request)

app.register_blueprint(auth_routes)
app.register_blueprint(profile_routes)
app.register_blueprint(social_routes)
app.register_blueprint(browse_routes)
app.register_blueprint(chat_routes)

if __name__ == "__main__":
    apply_schema()  # idempotent : crée les tables manquantes (dont messages)
    reset_all_online_status()  # purge les statuts en ligne laissés par l'instance précédente
    debug = is_debug_enabled()
    logger.info("Starting Matcha backend (debug=%s)", debug)
    socketio.run(app, host="0.0.0.0", port=5000, debug=debug)
