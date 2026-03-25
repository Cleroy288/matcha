from functools import wraps
from flask import request, jsonify
from services.jwt_service import decode_token
from utils.errors import ERR_TOKEN_MISSING


def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": ERR_TOKEN_MISSING}), 401

        try:
            payload = decode_token(token)
            return f(payload, *args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 401

    return decorated
