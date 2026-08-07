import re

VALID_GENDERS = {"male", "female", "other"}
VALID_PREFERENCES = {"male", "female", "bisexual"}
TAG_REGEX = re.compile(r"^#[a-zA-Z0-9-]+$")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

COMMON_PASSWORDS = {
    "password", "password123", "123456", "qwerty", "letmein"
}

EMAIL_MAX_LENGTH = 254
USERNAME_MAX_LENGTH = 32
PASSWORD_MIN_LENGTH = 8

BIO_MIN_LENGTH = 1
BIO_MAX_LENGTH = 500

MIN_AGE = 18
MAX_AGE = 120

TAG_NAME_MAX_LENGTH = 50

LATITUDE_MIN = -90
LATITUDE_MAX = 90
LONGITUDE_MIN = -180
LONGITUDE_MAX = 180

CITY_MIN_LENGTH = 1
CITY_MAX_LENGTH = 100

ALLOWED_IMAGE_EXTENSIONS = {
    ".jpg": "JPEG",
    ".jpeg": "JPEG",
    ".png": "PNG",
    ".webp": "WEBP",
}
ALLOWED_IMAGE_FORMATS = set(ALLOWED_IMAGE_EXTENSIONS.values())
MAX_FILE_SIZE = 5 * 1024 * 1024


# Tous les messages rendus à l'utilisateur sont en anglais, comme l'interface.
class AuthMessages:
    EMAIL_VERIFIED        = "Email verified. You can now log in."
    EMAIL_SEND_SUCCESS    = "Email sent. Click the link inside it to change your password."
    INVALID_EMAIL_FORMAT  = "Invalid email format"
    NOT_EMAIL             = "Email is missing"
    EMAIL_NOT_VERIFIED    = "Email is not verified"
    EMAIL_ALREADY_EXISTS   = "This email is already taken"

    PASSWORD_RESET_OK     = "Password changed. You can now log in."
    PASSWORD_INVALID      = "Invalid password"
    PASSWORD_INVALID_LEN  = f"Password must be at least {PASSWORD_MIN_LENGTH} characters"
    PASSWORD_INVALID_UP  = "Password must contain at least 1 uppercase letter"
    PASSWORD_INVALID_NUMBER  = "Password must contain at least 1 digit"
    PASSWORD_INVALID_SPECIAL  = "Password must contain at least 1 special character"
    PASSWORD_TOO_COMMON  = "Password is too weak: it contains a common word or common password"
    PASSWORDS_DO_NOT_MATCH = "Passwords do not match"

    NOT_TOKEN             = "Token is missing"
    INVALID_TOKEN         = "Invalid token"
    TOKEN_EXPIRED         = "Token has expired"
    USER_NOT_FOUND        = "User not found"
    USERNAME_ALREADY_EXISTS   = "This username is already taken"
    USERNAME_NOT_VALID    = f"Username must be at most {USERNAME_MAX_LENGTH} characters"

    REGISTER_SUCCES       = "Account created. Verify your email before logging in."
    REGISTER_SUCCESS_NO_EMAIL = "Account created. You can now log in."
    LOGIN_SUCCESS         = "Logged in."
    LOGOUT_SUCCESS        = "Logged out."
    ACCOUNT_DELETED       = "Account and personal data deleted."


class LikeMessage:
    LIKE_YOURSELF         = "You cannot like your own profile"
    LIKE_IMPOSSIBLE       = "Action not allowed"
    LIKE_ALREADY          = "Already liked"
