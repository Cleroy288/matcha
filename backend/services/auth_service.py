import os
import secrets

import bcrypt

from models.user_model import (
    confirm_user_email,
    create_user,
    get_user_by_email,
    get_user_by_username,
    get_user_by_verification_token,
    set_new_password,
    set_token_reset_password_user_email,
)
from services.email_service import send_reset_password_email, send_verification_email
from services.jwt_service import generate_token
from utils.auth_validator import validate_email, validate_password, validate_username
from utils.constants import AuthMessages


def email_verification_disabled():
    return os.getenv("DISABLE_EMAIL_VERIFICATION", "FALSE").upper() == "TRUE"

def register_user(email, username, password, confirm_password, first_name, last_name):

    if password != confirm_password:
        raise Exception(AuthMessages.PASSWORDS_DO_NOT_MATCH)

    if validate_email(email) is False:
        raise Exception(AuthMessages.INVALID_EMAIL_FORMAT)
    if validate_username(username) is False:
        raise Exception(AuthMessages.USERNAME_NOT_VALID)

    user_email =  get_user_by_email(email)
    if user_email:
        raise Exception(AuthMessages.EMAIL_ALREADY_EXISTS)

    user_username =  get_user_by_username(username)
    if user_username:
        raise Exception(AuthMessages.USERNAME_ALREADY_EXISTS)

    valid, error = validate_password(password)

    if not valid:
        raise Exception(error)

    skip_email_verification = email_verification_disabled()
    verification_token = None if skip_email_verification else secrets.token_urlsafe(32)

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    user_id = create_user(
        email,
        username,
        hashed.decode(),
        first_name,
        last_name,
        verification_token,
        email_verified=skip_email_verification
    )

    if not skip_email_verification:
        send_verification_email(email, verification_token)

    return user_id


def login_user(username, password):
    user =  get_user_by_username(username)
    if not user:
        raise Exception(AuthMessages.USER_NOT_FOUND)


    if not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        raise Exception(AuthMessages.PASSWORD_INVALID)
    if not user["email_verified"]:
        raise Exception(AuthMessages.EMAIL_NOT_VERIFIED)

    token = generate_token(user["id"])

    user_data = {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "profile_complete": user["profile_complete"],
    }

    return token, user_data


def verify_email_user(token):
    user = get_user_by_verification_token(token)
    if not user:
        raise Exception(AuthMessages.USER_NOT_FOUND)

    confirm_user_email(user['id'])


def reset_password_user(email):

    if validate_email(email) is False:
        raise Exception(AuthMessages.INVALID_EMAIL_FORMAT)
    user =  get_user_by_email(email)
    if not user:
        raise Exception(AuthMessages.USER_NOT_FOUND)
    if not user["email_verified"]:
        raise Exception(AuthMessages.EMAIL_NOT_VERIFIED)

    verification_token = secrets.token_urlsafe(32)
    set_token_reset_password_user_email(email, verification_token)
    send_reset_password_email(email, verification_token)


def verify_reset_password_user(token, password):
        valid, error = validate_password(password)
        if not valid:
            raise Exception(error)

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        user = set_new_password(hashed.decode(), token)
        if not user:
            raise Exception(AuthMessages.USER_NOT_FOUND)
