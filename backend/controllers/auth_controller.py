from flask import request, jsonify
from services.auth_service import register_user, login_user, reset_password_user, verify_reset_password_user, verify_email_user
from utils.jwt_required import jwt_required
from models.user_model import get_user_by_id
from controllers.constants import HTTP_OK, HTTP_CREATED, HTTP_BAD_REQUEST, HTTP_NOT_FOUND
from controllers.errors import (
    ERR_MISSING_TOKEN, ERR_MISSING_EMAIL, ERR_USER_NOT_FOUND,
    MSG_EMAIL_VERIFIED, MSG_PASSWORD_CHANGED, MSG_RESET_EMAIL_SENT
)


def register():
    data = request.json
    try:
        user_id = register_user(
            data["email"],
            data["username"],
            data["password"],
            data["first_name"],
            data["last_name"]
        )
        return jsonify({"user_id": user_id}), HTTP_CREATED
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST


def login():
    data = request.json
    try:
        username = data["username"]
        password = data["password"]
        token, user_data = login_user(username, password)
        return jsonify({"token": token, "user": user_data}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST


def verify_email():
    token = request.args.get('token')
    if not token:
        return jsonify({"error": ERR_MISSING_TOKEN}), HTTP_BAD_REQUEST

    try:
        verify_email_user(token)
        return jsonify({"message": MSG_EMAIL_VERIFIED}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST


def verify_reset_password():
    data = request.json
    token = request.args.get('token')
    if not token:
        return jsonify({"error": ERR_MISSING_TOKEN}), HTTP_BAD_REQUEST

    try:
        password = data["password"]
        verify_reset_password_user(token, password)
        return jsonify({"message": MSG_PASSWORD_CHANGED}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST


def reset_password():
    data = request.json
    try:
        email = data["email"]
        if not email:
            return jsonify({"error": ERR_MISSING_EMAIL}), HTTP_BAD_REQUEST
        reset_password_user(email)
        return jsonify({"message": MSG_RESET_EMAIL_SENT}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST


@jwt_required
def testmiddleware(payload):
    user_id = payload["user_id"]
    user = get_user_by_id(user_id)

    if not user:
        return jsonify({"error": ERR_USER_NOT_FOUND}), HTTP_NOT_FOUND

    return jsonify({
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }
    }), HTTP_OK
