from flask import jsonify
from utils.jwt_required import jwt_required
from utils.fame import recalculate_fame
from services.like_service import like_user, unlike_user, get_received_likes
from controllers.constants import HTTP_OK, HTTP_BAD_REQUEST

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