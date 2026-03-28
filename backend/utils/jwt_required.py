from functools import wraps
from flask import request, jsonify
from services.jwt_service import decode_token


def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("auth_token")

        if not token:
            return jsonify({"error": "Token missing"}), 401

        try:
            payload = decode_token(token)
            return f(payload, *args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 401

    return decorated