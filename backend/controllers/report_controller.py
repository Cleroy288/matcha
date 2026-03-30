from flask import jsonify, request
from utils.jwt_required import jwt_required
from services.report_service import report_user
from controllers.constants import HTTP_OK, HTTP_BAD_REQUEST

@jwt_required
def report(payload, user_id):
    data = request.get_json(silent=True) or {}
    reason = data.get("reason", None)
    try:
        report_user(payload["user_id"], int(user_id), reason)
        return jsonify({"reported": True}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST