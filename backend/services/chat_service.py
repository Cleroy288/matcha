from extensions import socketio
from models.block_model import is_blocked
from models.like_model import is_match
from models.message_model import (
    count_unread_messages,
    create_message,
    get_conversation_messages,
    get_conversations,
    mark_conversation_read,
)
from models.notification_model import create_notification
from services.constants import CONVERSATION_MESSAGES_LIMIT, MESSAGE_MAX_LENGTH
from services.errors import ERR_MESSAGE_EMPTY, ERR_MESSAGE_TOO_LONG, ERR_NOT_MATCHED
from services.socket_service import notify_user
from utils.photo_url import build_photo_url


def send_message(sender_id, receiver_id, content):
    """Envoie un message : vérifie le match, insère, notifie le destinataire
    en temps réel (event new_message + notification 'message')."""
    content = validate_content(content)
    ensure_can_chat(sender_id, receiver_id)

    message = create_message(sender_id, receiver_id, content)

    create_notification(receiver_id, sender_id, "message")
    notify_user(socketio, receiver_id, "message", {"from_user_id": sender_id})
    emit_new_message(receiver_id, message)

    return message


def get_messages(user_id, other_id):
    """Historique de la conversation ; marque les messages reçus comme lus."""
    ensure_can_chat(user_id, other_id)
    mark_conversation_read(user_id, other_id)
    return get_conversation_messages(user_id, other_id, CONVERSATION_MESSAGES_LIMIT)


def list_conversations(user_id):
    """Conversations = matchs, avec URL publique de la photo de profil."""
    conversations = get_conversations(user_id)
    for conversation in conversations:
        conversation["profile_photo_url"] = build_photo_url(conversation.pop("profile_photo"))
    return conversations


def get_unread_total(user_id):
    return count_unread_messages(user_id)


# ── Helpers ──

def ensure_can_chat(user_id, other_id):
    """Chat autorisé uniquement entre users connectés (match) et non bloqués (sujet IV.6)."""
    if user_id == other_id:
        raise Exception(ERR_NOT_MATCHED)
    if is_blocked(user_id, other_id):
        raise Exception(ERR_NOT_MATCHED)
    if not is_match(user_id, other_id):
        raise Exception(ERR_NOT_MATCHED)


def validate_content(content):
    """Message non vide et borné en taille."""
    content = (content or "").strip()
    if not content:
        raise Exception(ERR_MESSAGE_EMPTY)
    if len(content) > MESSAGE_MAX_LENGTH:
        raise Exception(ERR_MESSAGE_TOO_LONG)
    return content


def emit_new_message(receiver_id, message):
    """Pousse le message dans la room privée du destinataire (délai < 10s garanti)."""
    socketio.emit(
        "new_message",
        serialize_message(message),
        room=f"user_{receiver_id}"
    )


def serialize_message(message):
    """Timestamps → ISO pour le payload socket (jsonify ne passe pas par là)."""
    serialized = dict(message)
    if serialized.get("created_at") is not None:
        serialized["created_at"] = serialized["created_at"].isoformat()
    return serialized
