from flask import jsonify

from controllers.constants import HTTP_BAD_REQUEST, HTTP_OK
from services.like_service import get_received_likes, like_user, unlike_user
from utils.fame import recalculate_fame
from utils.jwt_required import jwt_required


@jwt_required
def like(payload, user_id):
    try:
        result = like_user(payload["user_id"], int(user_id))
        recalculate_fame()
        return jsonify(result), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST

@jwt_required
def unlike(payload, user_id):
    try:
        result = unlike_user(payload["user_id"], int(user_id))
        recalculate_fame()
        return jsonify(result), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST

@jwt_required
def likes_received(payload):
    try:
        likes = get_received_likes(payload["user_id"])
        return jsonify({"likes": likes}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST