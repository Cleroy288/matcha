import re
from utils.constants import AuthMessages 

EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)

def validate_email(email):
    if len(email) > 254:
        return False
    return bool(EMAIL_REGEX.fullmatch(email))

def validate_username(username):
    if len(username) > 32:
        return False
    return True

def validate_password(password):

    if len(password) < 8:
        return False, AuthMessages.PASSWORD_INVALID_LEN

    if not re.search(r"[A-Z]", password):
        return False, AuthMessages.PASSWORD_INVALID_UP

    if not re.search(r"[0-9]", password):
        return False, AuthMessages.PASSWORD_INVALID_NUMBER

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, AuthMessages.PASSWORD_INVALID_SPECIAL

    return True, None