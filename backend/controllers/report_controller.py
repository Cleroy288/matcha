from flask import jsonify, request

from controllers.constants import HTTP_BAD_REQUEST, HTTP_OK
from services.report_service import report_user
from utils.fame import recalculate_fame
from utils.jwt_required import jwt_required


@jwt_required
def report(payload, user_id):
    data = request.get_json(silent=True) or {}
    reason = data.get("reason", None)
    try:
        report_user(payload["user_id"], int(user_id), reason)
        recalculate_fame()
        return jsonify({"reported": True}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST