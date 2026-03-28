import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from utils.auth_validator import validate_email, validate_password, validate_username
from utils.errors import (
    ERR_INVALID_EMAIL,
    ERR_PASSWORD_NO_NUMBER,
    ERR_PASSWORD_NO_SPECIAL,
    ERR_PASSWORD_NO_UPPERCASE,
    ERR_PASSWORD_TOO_COMMON,
    ERR_PASSWORD_TOO_SHORT,
    ERR_USERNAME_TOO_LONG,
)


class TestValidateEmail:
    def test_valid_email(self):
        valid, error = validate_email("user@example.com")
        assert valid is True
        assert error is None

    def test_email_without_at(self):
        valid, error = validate_email("invalid-email")
        assert valid is False
        assert error == ERR_INVALID_EMAIL

    def test_email_too_long(self):
        long_email = "a" * 250 + "@b.com"
        valid, error = validate_email(long_email)
        assert valid is False
        assert error == ERR_INVALID_EMAIL


class TestValidateUsername:
    def test_valid_username(self):
        valid, error = validate_username("johndoe")
        assert valid is True
        assert error is None

    def test_username_too_long(self):
        valid, error = validate_username("a" * 33)
        assert valid is False
        assert error == ERR_USERNAME_TOO_LONG


class TestValidatePassword:
    def test_valid_password(self):
        valid, error = validate_password("StrongP@ss1")
        assert valid is True
        assert error is None

    def test_password_too_short(self):
        valid, error = validate_password("Sh0rt!")
        assert valid is False
        assert error == ERR_PASSWORD_TOO_SHORT

    def test_password_no_uppercase(self):
        valid, error = validate_password("nouppercas3!")
        assert valid is False
        assert error == ERR_PASSWORD_NO_UPPERCASE

    def test_password_no_number(self):
        valid, error = validate_password("NoNumberHere!")
        assert valid is False
        assert error == ERR_PASSWORD_NO_NUMBER

    def test_password_no_special(self):
        valid, error = validate_password("NoSpecial1here")
        assert valid is False
        assert error == ERR_PASSWORD_NO_SPECIAL

    def test_password_too_common(self, mocker):
        mocker.patch("utils.auth_validator.COMMON_PASSWORDS", {"strongp@ss1"})
        valid, error = validate_password("StrongP@ss1")
        assert valid is False
        assert error == ERR_PASSWORD_TOO_COMMON
