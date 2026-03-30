from flask import jsonify
from utils.jwt_required import jwt_required
from services.profile_view_service import view_profile, get_profile_views
from controllers.constants import HTTP_OK, HTTP_BAD_REQUEST

@jwt_required
def visit(payload, user_id):
    try:
        view_profile(payload["user_id"], int(user_id))
        return jsonify({"visited": True}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST

@jwt_required
def views_received(payload):
    try:
        views = get_profile_views(payload["user_id"])
        return jsonify({"views": views}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST