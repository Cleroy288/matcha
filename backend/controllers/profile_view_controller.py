from flask import jsonify

from controllers.constants import HTTP_BAD_REQUEST, HTTP_OK
from services.profile_view_service import get_profile_views, view_profile
from utils.fame import recalculate_fame
from utils.jwt_required import jwt_required


@jwt_required
def visit(payload, user_id):
    try:
        view_profile(payload["user_id"], int(user_id))
        recalculate_fame()
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