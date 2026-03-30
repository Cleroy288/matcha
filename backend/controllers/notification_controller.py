from flask import jsonify
from utils.jwt_required import jwt_required
from services.notification_service import get_user_notifications, mark_notifications_read, get_unread_count
from controllers.constants import HTTP_OK, HTTP_BAD_REQUEST

@jwt_required
def get_notifications(payload):
    try:
        notifs = get_user_notifications(payload["user_id"])
        return jsonify({"notifications": notifs}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST

@jwt_required
def read_notifications(payload):
    try:
        mark_notifications_read(payload["user_id"])
        return jsonify({"ok": True}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST

@jwt_required
def unread_count(payload):
    try:
        count = get_unread_count(payload["user_id"])
        return jsonify({"count": count}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST