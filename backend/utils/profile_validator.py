from datetime import datetime, date
from utils.constants import (
    VALID_GENDERS, VALID_PREFERENCES, TAG_REGEX,
    BIO_MIN_LENGTH, BIO_MAX_LENGTH,
    MIN_AGE, MAX_AGE,
    TAG_NAME_MAX_LENGTH,
    LATITUDE_MIN, LATITUDE_MAX, LONGITUDE_MIN, LONGITUDE_MAX,
    CITY_MIN_LENGTH, CITY_MAX_LENGTH
)
from utils.errors import (
    ERR_INVALID_GENDER, ERR_INVALID_PREFERENCE, ERR_INVALID_BIO,
    ERR_INVALID_BIRTH_DATE_FORMAT, ERR_TOO_YOUNG, ERR_INVALID_BIRTH_DATE,
    ERR_INVALID_TAG_LENGTH, ERR_INVALID_TAG_FORMAT,
    ERR_INVALID_COORDINATES, ERR_INVALID_LATITUDE, ERR_INVALID_LONGITUDE,
    ERR_INVALID_CITY
)


def validate_gender(gender):
    if gender not in VALID_GENDERS:
        return False, ERR_INVALID_GENDER
    return True, None


def validate_sexual_preference(pref):
    if pref not in VALID_PREFERENCES:
        return False, ERR_INVALID_PREFERENCE
    return True, None


def validate_biography(bio):
    bio = bio.strip()
    if len(bio) < BIO_MIN_LENGTH or len(bio) > BIO_MAX_LENGTH:
        return False, ERR_INVALID_BIO
    return True, None


def validate_birth_date(date_str):
    try:
        birth = datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return False, ERR_INVALID_BIRTH_DATE_FORMAT

    today = date.today()
    age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

    if age < MIN_AGE:
        return False, ERR_TOO_YOUNG
    if age > MAX_AGE:
        return False, ERR_INVALID_BIRTH_DATE

    return True, None


def validate_tag_name(name):
    if not name or len(name) > TAG_NAME_MAX_LENGTH:
        return False, ERR_INVALID_TAG_LENGTH
    if not TAG_REGEX.fullmatch(name):
        return False, ERR_INVALID_TAG_FORMAT
    return True, None


def validate_location(lat, lng):
    try:
        lat = float(lat)
        lng = float(lng)
    except (ValueError, TypeError):
        return False, ERR_INVALID_COORDINATES

    if lat < LATITUDE_MIN or lat > LATITUDE_MAX:
        return False, ERR_INVALID_LATITUDE
    if lng < LONGITUDE_MIN or lng > LONGITUDE_MAX:
        return False, ERR_INVALID_LONGITUDE

    return True, None


def validate_city(city):
    city = city.strip()
    if len(city) < CITY_MIN_LENGTH or len(city) > CITY_MAX_LENGTH:
        return False, ERR_INVALID_CITY
    return True, None
