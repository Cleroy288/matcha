import logging

from flask_socketio import join_room, leave_room

from models.profile_model import set_online_status
from services.jwt_service import decode_token
from services.profile_service import get_or_create_profile

logger = logging.getLogger(__name__)

# A user can open several tabs: every socket is kept so the user only goes
# offline once the last one is closed.
connected_users = {}  # { user_id: set(socket_id) }


def handle_connect(socketio, request):
    """Called when a user opens a WebSocket connection: private room + online status."""
    try:
        # Read the token from the WS connection cookies
        token = request.cookies.get("auth_token")
        if not token:
            return False  # refuse the connection

        payload = decode_token(token)
        user_id = payload["user_id"]

        # The user joins their private room
        join_room(f"user_{user_id}")
        register_socket(user_id, request.sid)
        logger.info("User %s connected via WebSocket", user_id)

    except Exception:
        # tells an invalid token apart from a real failure (DB, network) in the logs
        logger.warning("WebSocket connection refused", exc_info=True)
        return False  # token invalide → refuse


def handle_disconnect(request):
    """Called when a user closes a tab: offline once the last tab is closed."""
    user_id = find_user_by_socket(request.sid)
    # 1 socket refused at connection time (invalid token): nothing to clean up
    if user_id is None:
        return

    leave_room(f"user_{user_id}")
    unregister_socket(user_id, request.sid)
    logger.info("User %s disconnected", user_id)


def register_socket(user_id, sid):
    """Registers a tab; only goes back online on the very first one opened."""
    sockets = connected_users.setdefault(user_id, set())
    is_first_socket = len(sockets) == 0
    sockets.add(sid)

    if not is_first_socket:
        return

    # the profiles row is created lazily: without it the status UPDATE would
    # touch no row and the user would never show up as "online"
    get_or_create_profile(user_id)
    set_online_status(user_id, True)


def unregister_socket(user_id, sid):
    """Removes a tab; only goes offline once the last one is closed."""
    sockets = connected_users.get(user_id)
    # 1 tabs already purged by an explicit logout
    if sockets is None:
        return

    sockets.discard(sid)
    # 2 other tabs are still open: the user is still online
    if sockets:
        return

    del connected_users[user_id]
    set_online_status(user_id, False)


def disconnect_user(user_id):
    """Forces the offline status at logout, without waiting for the sockets to close."""
    connected_users.pop(user_id, None)
    set_online_status(user_id, False)


def find_user_by_socket(sid):
    """Owner of a socket; None if the socket was never registered."""
    return next(
        (user_id for user_id, sockets in connected_users.items() if sid in sockets),
        None
    )


def notify_user(socketio, user_id, notif_type, data=None):
    """Sends a real-time notification to a specific user."""
    socketio.emit(
        "new_notification",
        {"type": notif_type, "data": data or {}},
        room=f"user_{user_id}"
    )