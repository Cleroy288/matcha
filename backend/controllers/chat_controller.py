from flask import jsonify, request

from controllers.constants import HTTP_BAD_REQUEST, HTTP_CREATED, HTTP_OK
from services.chat_service import get_messages, get_unread_total, list_conversations, send_message
from utils.jwt_required import jwt_required


@jwt_required
def conversations(payload):
    """GET /chat/conversations — liste des matchs avec dernier message."""
    try:
        result = list_conversations(payload["user_id"])
        return jsonify({"conversations": result}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST


@jwt_required
def conversation_messages(payload, user_id):
    """GET /chat/messages/<user_id> — historique + marque comme lus."""
    try:
        messages = get_messages(payload["user_id"], int(user_id))
        return jsonify({"messages": messages}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST


@jwt_required
def post_message(payload, user_id):
    """POST /chat/messages/<user_id> — envoie un message au match."""
    data = request.json or {}
    try:
        message = send_message(payload["user_id"], int(user_id), data.get("content"))
        return jsonify(message), HTTP_CREATED
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST


@jwt_required
def unread_messages(payload):
    """GET /chat/unread — total de messages non lus (badge toutes pages)."""
    try:
        count = get_unread_total(payload["user_id"])
        return jsonify({"count": count}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST
