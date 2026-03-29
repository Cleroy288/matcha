from flask_socketio import emit, join_room, leave_room
from services.jwt_service import decode_token

connected_users = {}  # { user_id: socket_id }

def handle_connect(socketio, request):
    """Appelé quand un user ouvre une connexion WebSocket."""
    try:
        # On récupère le token depuis les cookies de la connexion WS
        token = request.cookies.get("auth_token")
        if not token:
            return False  # refuse la connexion

        payload = decode_token(token)
        user_id = payload["user_id"]

        # L'user rejoint sa room privée
        join_room(f"user_{user_id}")
        connected_users[user_id] = request.sid  # sid = socket id unique
        print(f"User {user_id} connecté via WebSocket")

    except Exception:
        return False  # token invalide → refuse


def handle_disconnect(request):
    """Appelé quand un user ferme la connexion."""
    sid = request.sid
    # Retrouve le user_id depuis le sid
    user_id = next((uid for uid, s in connected_users.items() if s == sid), None)
    if user_id:
        leave_room(f"user_{user_id}")
        del connected_users[user_id]
        print(f"User {user_id} déconnecté")


def notify_user(socketio, user_id, notif_type, data=None):
    """Envoie une notification temps réel à un user spécifique."""
    socketio.emit(
        "new_notification",
        {"type": notif_type, "data": data or {}},
        room=f"user_{user_id}"
    )