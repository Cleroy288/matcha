from flask import jsonify

from controllers.constants import HTTP_BAD_REQUEST, HTTP_OK
from services.block_service import block_user, unblock_user
from utils.jwt_required import jwt_required


@jwt_required
def block(payload, user_id):
    try:
        block_user(payload["user_id"], int(user_id))
        return jsonify({"blocked": True}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST

@jwt_required
def unblock(payload, user_id):
    try:
        unblock_user(payload["user_id"], int(user_id))
        return jsonify({"unblocked": True}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST