import logging

from flask import jsonify, make_response, request

from controllers.constants import HTTP_BAD_REQUEST, HTTP_CREATED, HTTP_NOT_FOUND, HTTP_OK
from models.user_model import get_user_by_id
from services.auth_service import (
    email_verification_disabled,
    login_user,
    register_user,
    reset_password_user,
    verify_email_user,
    verify_reset_password_user,
)
from services.jwt_service import decode_token
from services.socket_service import disconnect_user
from utils.constants import AuthMessages
from utils.jwt_required import jwt_required
from utils.request_body import get_json_body, require_fields

logger = logging.getLogger(__name__)

REGISTER_REQUIRED_FIELDS = ("email", "username", "password", "first_name", "last_name")
COOKIE_MAX_AGE_S = 3600


def register():
    try:
        data = get_json_body()
        require_fields(data, *REGISTER_REQUIRED_FIELDS)

        register_user(
            data["email"],
            data["username"],
            data["password"],
            data.get("confirm_password"),
            data["first_name"],
            data["last_name"]
        )

        requires_email_verification = not email_verification_disabled()
        message = AuthMessages.REGISTER_SUCCES if requires_email_verification else AuthMessages.REGISTER_SUCCESS_NO_EMAIL
        return jsonify({
            "message": message,
            "email_verification_required": requires_email_verification,
        }), HTTP_CREATED

    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST


def login():
    try:
        data = get_json_body()
        require_fields(data, "username", "password")

        token, user_data = login_user(data["username"], data["password"])

        response = make_response(jsonify({
            "message": AuthMessages.LOGIN_SUCCESS,
            "user": user_data
        }), HTTP_OK)

        response.set_cookie(
            "auth_token",
            value=token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=COOKIE_MAX_AGE_S
        )

        return response

    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST


def logout():
    force_offline_from_cookie()
    response = make_response(jsonify({"message": AuthMessages.LOGOUT_SUCCESS}), HTTP_OK)
    response.delete_cookie("auth_token")
    return response


def force_offline_from_cookie():
    """Passe l'user hors ligne dès le logout : le socket peut mettre plusieurs
    secondes à se fermer, voire rester ouvert si l'onglet n'est pas fermé."""
    token = request.cookies.get("auth_token")
    # 1 session déjà expirée côté client : il n'y a plus de statut à corriger
    if not token:
        return

    try:
        disconnect_user(decode_token(token)["user_id"])
    except Exception:
        # 2 token illisible : on supprime quand même le cookie, sans toucher au statut
        logger.info("Logout with an unusable token, online status left untouched")


def verify_email():
    token = request.args.get('token')
    if not token:
        return jsonify({"error": AuthMessages.NOT_TOKEN}), HTTP_BAD_REQUEST

    try:
        verify_email_user(token)
        return jsonify({"message": AuthMessages.EMAIL_VERIFIED}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST


def verify_reset_password():
    token = request.args.get('token')
    if not token:
        return jsonify({"error": AuthMessages.NOT_TOKEN}), HTTP_BAD_REQUEST

    try:
        data = get_json_body()
        require_fields(data, "password")

        verify_reset_password_user(token, data["password"])
        return jsonify({"message": AuthMessages.PASSWORD_RESET_OK}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST


def reset_password():
    try:
        data = get_json_body()
        require_fields(data, "email")

        reset_password_user(data["email"])
        return jsonify({"message": AuthMessages.EMAIL_SEND_SUCCESS}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST


# TEST ca va disparaitre
@jwt_required # A mettre au dessus d'un controller pour proteger sa route
def testmiddleware(payload):
    user_id = payload["user_id"]
    user = get_user_by_id(user_id)

    if not user:
        return jsonify({"error": AuthMessages.USER_NOT_FOUND}), HTTP_NOT_FOUND

    return jsonify({
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }
    })
