from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os
from database.db import get_connection
from routes.auth_routes import auth_routes

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def index():
    return "Matcha Backend fonctionne !"

@app.route("/test-db")
def test_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT 1")

    result = cur.fetchone()

    cur.close()
    conn.close()

    return {"db": result}

app.register_blueprint(auth_routes)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
    # debug=True active le refresh automatique