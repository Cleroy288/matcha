import logging

from flask_socketio import join_room, leave_room

from models.profile_model import set_online_status
from services.jwt_service import decode_token
from services.profile_service import get_or_create_profile

logger = logging.getLogger(__name__)

# Un user peut ouvrir plusieurs onglets : on garde tous ses sockets pour ne le
# passer hors ligne qu'à la fermeture du dernier.
connected_users = {}  # { user_id: set(socket_id) }


def handle_connect(socketio, request):
    """Appelé quand un user ouvre une connexion WebSocket : room privée + statut en ligne."""
    try:
        # On récupère le token depuis les cookies de la connexion WS
        token = request.cookies.get("auth_token")
        if not token:
            return False  # refuse la connexion

        payload = decode_token(token)
        user_id = payload["user_id"]

        # L'user rejoint sa room privée
        join_room(f"user_{user_id}")
        register_socket(user_id, request.sid)
        logger.info("User %s connected via WebSocket", user_id)

    except Exception:
        # distingue dans les logs un token invalide d'une vraie panne (DB, réseau)
        logger.warning("WebSocket connection refused", exc_info=True)
        return False  # token invalide → refuse


def handle_disconnect(request):
    """Appelé quand un user ferme un onglet : hors ligne au dernier onglet fermé."""
    user_id = find_user_by_socket(request.sid)
    # 1 socket refusé à la connexion (token invalide) : rien à nettoyer
    if user_id is None:
        return

    leave_room(f"user_{user_id}")
    unregister_socket(user_id, request.sid)
    logger.info("User %s disconnected", user_id)


def register_socket(user_id, sid):
    """Enregistre un onglet ; ne repasse en ligne qu'au tout premier ouvert."""
    sockets = connected_users.setdefault(user_id, set())
    is_first_socket = len(sockets) == 0
    sockets.add(sid)

    if not is_first_socket:
        return

    # la ligne profiles est créée paresseusement : sans elle, l'UPDATE du statut
    # ne toucherait aucune ligne et l'user resterait invisible comme "en ligne"
    get_or_create_profile(user_id)
    set_online_status(user_id, True)


def unregister_socket(user_id, sid):
    """Retire un onglet ; ne passe hors ligne qu'une fois le dernier fermé."""
    sockets = connected_users.get(user_id)
    # 1 onglets déjà purgés par un logout explicite
    if sockets is None:
        return

    sockets.discard(sid)
    # 2 d'autres onglets restent ouverts : l'user est toujours en ligne
    if sockets:
        return

    del connected_users[user_id]
    set_online_status(user_id, False)


def disconnect_user(user_id):
    """Force le statut hors ligne au logout, sans attendre la fermeture des sockets."""
    connected_users.pop(user_id, None)
    set_online_status(user_id, False)


def find_user_by_socket(sid):
    """Propriétaire d'un socket ; None si le socket n'a jamais été enregistré."""
    return next(
        (user_id for user_id, sockets in connected_users.items() if sid in sockets),
        None
    )


def notify_user(socketio, user_id, notif_type, data=None):
    """Envoie une notification temps réel à un user spécifique."""
    socketio.emit(
        "new_notification",
        {"type": notif_type, "data": data or {}},
        room=f"user_{user_id}"
    )