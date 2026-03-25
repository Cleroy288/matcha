import re
from utils.constants import (
    COMMON_PASSWORDS, EMAIL_REGEX,
    EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH, PASSWORD_MIN_LENGTH
)
from utils.errors import (
    ERR_PASSWORD_TOO_SHORT, ERR_PASSWORD_NO_UPPERCASE,
    ERR_PASSWORD_NO_NUMBER, ERR_PASSWORD_NO_SPECIAL,
    ERR_PASSWORD_TOO_COMMON, ERR_INVALID_EMAIL, ERR_USERNAME_TOO_LONG
)


def validate_email(email):
    if len(email) > EMAIL_MAX_LENGTH:
        return False, ERR_INVALID_EMAIL
    if not EMAIL_REGEX.fullmatch(email):
        return False, ERR_INVALID_EMAIL
    return True, None


def validate_username(username):
    if len(username) > USERNAME_MAX_LENGTH:
        return False, ERR_USERNAME_TOO_LONG
    return True, None


def validate_password(password):
    if len(password) < PASSWORD_MIN_LENGTH:
        return False, ERR_PASSWORD_TOO_SHORT

    if not re.search(r"[A-Z]", password):
        return False, ERR_PASSWORD_NO_UPPERCASE

    if not re.search(r"[0-9]", password):
        return False, ERR_PASSWORD_NO_NUMBER

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, ERR_PASSWORD_NO_SPECIAL

    if password.lower() in COMMON_PASSWORDS:
        return False, ERR_PASSWORD_TOO_COMMON

    return True, None
