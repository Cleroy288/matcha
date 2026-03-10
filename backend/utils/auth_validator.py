import re

COMMON_PASSWORDS = {
    "password",
    "password123",
    "123456",
    "qwerty",
    "letmein"
} #trouver une liste des mot basique en anglais (sujet)

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
        return False, "Password must be at least 8 characters"

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain an uppercase letter"

    if not re.search(r"[0-9]", password):
        return False, "Password must contain a number"

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain a special character"

    if password.lower() in COMMON_PASSWORDS:
        return False, "Password too common"

    return True, None