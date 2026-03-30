from flask import Flask, request as flask_request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from extensions import socketio
from routes.auth_routes import auth_routes
from routes.profile_routes import profile_routes
from routes.social_routes import social_routes
from services.socket_service import handle_connect, handle_disconnect

load_dotenv()

app = Flask(__name__)

CORS(app, supports_credentials=True, origins=["http://localhost:5173"])
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

socketio.init_app(
    app,
    cors_allowed_origins="http://localhost:5173",
    manage_session=False
)

@app.route("/")
def index():
    return "Matcha Backend fonctionne !"

@socketio.on("connect")
def on_connect():
    handle_connect(socketio, flask_request)

@socketio.on("disconnect")
def on_disconnect():
    handle_disconnect(flask_request)

app.register_blueprint(auth_routes)
app.register_blueprint(profile_routes)
app.register_blueprint(social_routes)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
    # debug=True active le refresh automatique