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

ALLOWED_IMAGE_FORMATS = {"JPEG", "PNG", "WEBP"}
MAX_FILE_SIZE = 5 * 1024 * 1024
DEFAULT_IMAGE_EXTENSION = ".jpg"
