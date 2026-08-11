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
    """Sends a message: checks the match, inserts it, then notifies the
    recipient in real time (new_message event + 'message' notification)."""
    content = validate_content(content)
    ensure_can_chat(sender_id, receiver_id)

    message = create_message(sender_id, receiver_id, content)

    create_notification(receiver_id, sender_id, "message")
    notify_user(socketio, receiver_id, "message", {"from_user_id": sender_id})
    emit_new_message(receiver_id, message)

    return message


def get_messages(user_id, other_id):
    """Conversation history; marks the received messages as read."""
    ensure_can_chat(user_id, other_id)
    mark_conversation_read(user_id, other_id)
    return get_conversation_messages(user_id, other_id, CONVERSATION_MESSAGES_LIMIT)


def list_conversations(user_id):
    """Conversations = matches, with the public URL of the profile photo."""
    conversations = get_conversations(user_id)
    for conversation in conversations:
        conversation["profile_photo_url"] = build_photo_url(conversation.pop("profile_photo"))
    return conversations


def get_unread_total(user_id):
    return count_unread_messages(user_id)


# ── Helpers ──

def ensure_can_chat(user_id, other_id):
    """Chat allowed only between connected users (match) who are not blocked (subject IV.6)."""
    if user_id == other_id:
        raise Exception(ERR_NOT_MATCHED)
    if is_blocked(user_id, other_id):
        raise Exception(ERR_NOT_MATCHED)
    if not is_match(user_id, other_id):
        raise Exception(ERR_NOT_MATCHED)


def validate_content(content):
    """Message must be non-empty and within the size limit."""
    content = (content or "").strip()
    if not content:
        raise Exception(ERR_MESSAGE_EMPTY)
    if len(content) > MESSAGE_MAX_LENGTH:
        raise Exception(ERR_MESSAGE_TOO_LONG)
    return content


def emit_new_message(receiver_id, message):
    """Pushes the message into the recipient private room (< 10s guaranteed)."""
    socketio.emit(
        "new_message",
        serialize_message(message),
        room=f"user_{receiver_id}"
    )


def serialize_message(message):
    """Timestamps → ISO for the socket payload (jsonify is not involved here)."""
    serialized = dict(message)
    if serialized.get("created_at") is not None:
        serialized["created_at"] = serialized["created_at"].isoformat()
    return serialized
