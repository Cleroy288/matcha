import os
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from utils.errors import (
    ERR_INVALID_BIO,
    ERR_INVALID_BIRTH_DATE,
    ERR_INVALID_BIRTH_DATE_FORMAT,
    ERR_INVALID_CITY,
    ERR_INVALID_COORDINATES,
    ERR_INVALID_GENDER,
    ERR_INVALID_LATITUDE,
    ERR_INVALID_LONGITUDE,
    ERR_INVALID_PREFERENCE,
    ERR_INVALID_TAG_FORMAT,
    ERR_INVALID_TAG_LENGTH,
    ERR_TOO_YOUNG,
)
from utils.profile_validator import (
    validate_biography,
    validate_birth_date,
    validate_city,
    validate_gender,
    validate_location,
    validate_sexual_preference,
    validate_tag_name,
)


class TestValidateGender:
    def test_valid_gender(self):
        valid, error = validate_gender("male")
        assert valid is True
        assert error is None

    def test_invalid_gender(self):
        valid, error = validate_gender("alien")
        assert valid is False
        assert error == ERR_INVALID_GENDER


class TestValidateSexualPreference:
    def test_valid_preference(self):
        valid, error = validate_sexual_preference("bisexual")
        assert valid is True
        assert error is None

    def test_invalid_preference(self):
        valid, error = validate_sexual_preference("asexual")
        assert valid is False
        assert error == ERR_INVALID_PREFERENCE


class TestValidateBiography:
    def test_valid_biography(self):
        valid, error = validate_biography("Hello world")
        assert valid is True
        assert error is None

    def test_empty_biography(self):
        valid, error = validate_biography("   ")
        assert valid is False
        assert error == ERR_INVALID_BIO

    def test_biography_too_long(self):
        valid, error = validate_biography("x" * 501)
        assert valid is False
        assert error == ERR_INVALID_BIO


class TestValidateBirthDate:
    def test_valid_birth_date(self):
        valid, error = validate_birth_date("2000-01-01")
        assert valid is True
        assert error is None

    def test_too_young(self):
        recent = date.today() - timedelta(days=365 * 17)
        valid, error = validate_birth_date(recent.strftime("%Y-%m-%d"))
        assert valid is False
        assert error == ERR_TOO_YOUNG

    def test_invalid_format(self):
        valid, error = validate_birth_date("01/01/2000")
        assert valid is False
        assert error == ERR_INVALID_BIRTH_DATE_FORMAT

    def test_too_old(self):
        valid, error = validate_birth_date("1800-01-01")
        assert valid is False
        assert error == ERR_INVALID_BIRTH_DATE


class TestValidateTagName:
    def test_valid_tag(self):
        valid, error = validate_tag_name("#python")
        assert valid is True
        assert error is None

    def test_tag_without_hash(self):
        valid, error = validate_tag_name("python")
        assert valid is False
        assert error == ERR_INVALID_TAG_FORMAT

    def test_empty_tag(self):
        valid, error = validate_tag_name("")
        assert valid is False
        assert error == ERR_INVALID_TAG_LENGTH

    def test_tag_too_long(self):
        valid, error = validate_tag_name("#" + "a" * 50)
        assert valid is False
        assert error == ERR_INVALID_TAG_LENGTH


class TestValidateLocation:
    def test_valid_location(self):
        valid, error = validate_location(48.8566, 2.3522)
        assert valid is True
        assert error is None

    def test_invalid_latitude(self):
        valid, error = validate_location(200, 2.3522)
        assert valid is False
        assert error == ERR_INVALID_LATITUDE

    def test_invalid_longitude(self):
        valid, error = validate_location(48.8, 300)
        assert valid is False
        assert error == ERR_INVALID_LONGITUDE

    def test_non_numeric_coordinates(self):
        valid, error = validate_location("abc", "def")
        assert valid is False
        assert error == ERR_INVALID_COORDINATES


class TestValidateCity:
    def test_valid_city(self):
        valid, error = validate_city("Paris")
        assert valid is True
        assert error is None

    def test_empty_city(self):
        valid, error = validate_city("   ")
        assert valid is False
        assert error == ERR_INVALID_CITY

    def test_city_too_long(self):
        valid, error = validate_city("x" * 101)
        assert valid is False
        assert error == ERR_INVALID_CITY
