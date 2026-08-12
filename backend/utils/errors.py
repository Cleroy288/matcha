from utils.constants import (
    BIO_MAX_LENGTH,
    BIO_MIN_LENGTH,
    CITY_MAX_LENGTH,
    CITY_MIN_LENGTH,
    LATITUDE_MAX,
    LATITUDE_MIN,
    LONGITUDE_MAX,
    LONGITUDE_MIN,
    MAX_FILE_SIZE,
    MIN_AGE,
    PASSWORD_MIN_LENGTH,
    TAG_NAME_MAX_LENGTH,
)

ERR_INVALID_GENDER = "Gender must be male, female, or other"
ERR_INVALID_PREFERENCE = "Preference must be male, female, or bisexual"
ERR_INVALID_BIO = f"Biography must be between {BIO_MIN_LENGTH} and {BIO_MAX_LENGTH} characters"
ERR_INVALID_BIRTH_DATE_FORMAT = "Birth date must be in YYYY-MM-DD format"
ERR_TOO_YOUNG = f"You must be at least {MIN_AGE} years old"
ERR_INVALID_BIRTH_DATE = "Invalid birth date"
ERR_INVALID_TAG_LENGTH = f"Tag must be between 1 and {TAG_NAME_MAX_LENGTH} characters"
ERR_INVALID_TAG_FORMAT = "Tag must start with # and contain only letters, numbers, and hyphens"
ERR_INVALID_COORDINATES = "Latitude and longitude must be numbers"
ERR_INVALID_LATITUDE = f"Latitude must be between {LATITUDE_MIN} and {LATITUDE_MAX}"
ERR_INVALID_LONGITUDE = f"Longitude must be between {LONGITUDE_MIN} and {LONGITUDE_MAX}"
ERR_INVALID_CITY = f"City must be between {CITY_MIN_LENGTH} and {CITY_MAX_LENGTH} characters"

ERR_NO_FILE = "No file provided"
ERR_INVALID_IMAGE = "File is not a valid image"
ERR_INVALID_IMAGE_FORMAT = "Image format must be JPEG, PNG, or WEBP"
ERR_INVALID_IMAGE_EXTENSION = "Image extension must match its JPEG, PNG, or WEBP content"
ERR_IMAGE_TOO_LARGE = f"Image must be under {MAX_FILE_SIZE // (1024 * 1024)}MB"

ERR_PASSWORD_TOO_SHORT = f"Password must be at least {PASSWORD_MIN_LENGTH} characters"
ERR_PASSWORD_NO_UPPERCASE = "Password must contain an uppercase letter"
ERR_PASSWORD_NO_NUMBER = "Password must contain a number"
ERR_PASSWORD_NO_SPECIAL = "Password must contain a special character"
ERR_PASSWORD_TOO_COMMON = "Password too common"

ERR_INVALID_EMAIL = "Invalid email format"
ERR_USERNAME_TOO_LONG = "Username too long"

ERR_TOKEN_MISSING = "Token missing"
