from flask import jsonify

from controllers.constants import HTTP_BAD_REQUEST, HTTP_OK
from services.report_service import report_user
from utils.fame import recalculate_fame
from utils.jwt_required import jwt_required
from utils.request_body import get_json_body


@jwt_required
def report(payload, user_id):
    try:
        data = get_json_body()
        report_user(payload["user_id"], int(user_id), data.get("reason"))
        recalculate_fame()
        return jsonify({"reported": True}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST