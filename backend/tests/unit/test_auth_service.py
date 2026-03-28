import os
import sys

import bcrypt
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest-32bytes!")
os.environ.setdefault("FRONTEND_URL", "http://localhost:5173")

from services.auth_service import (
    login_user,
    register_user,
    reset_password_user,
    verify_email_user,
    verify_reset_password_user,
)
from services.errors import (
    ERR_EMAIL_ALREADY_REGISTERED,
    ERR_EMAIL_NOT_REGISTERED,
    ERR_EMAIL_NOT_VERIFIED,
    ERR_INVALID_LINK,
    ERR_INVALID_PASSWORD,
    ERR_USERNAME_ALREADY_TAKEN,
    ERR_USERNAME_NOT_REGISTERED,
)

VALID_PASSWORD = "StrongP@ss1"
VALID_HASHED = bcrypt.hashpw(VALID_PASSWORD.encode(), bcrypt.gensalt()).decode()


class TestRegisterUser:
    def test_success(self, mocker):
        mocker.patch("services.auth_service.get_user_by_email", return_value=None)
        mocker.patch("services.auth_service.get_user_by_username", return_value=None)
        mocker.patch("services.auth_service.create_user", return_value=1)
        mocker.patch("services.auth_service.send_verification_email")

        user_id = register_user("new@test.com", "newuser", VALID_PASSWORD, "New", "User")
        assert user_id == 1

    def test_email_already_registered(self, mocker):
        mocker.patch("services.auth_service.get_user_by_email", return_value={"id": 1})

        with pytest.raises(Exception, match=ERR_EMAIL_ALREADY_REGISTERED):
            register_user("taken@test.com", "newuser", VALID_PASSWORD, "New", "User")

    def test_username_already_taken(self, mocker):
        mocker.patch("services.auth_service.get_user_by_email", return_value=None)
        mocker.patch("services.auth_service.get_user_by_username", return_value={"id": 2})

        with pytest.raises(Exception, match=ERR_USERNAME_ALREADY_TAKEN):
            register_user("new@test.com", "taken", VALID_PASSWORD, "New", "User")

    def test_invalid_password(self, mocker):
        mocker.patch("services.auth_service.get_user_by_email", return_value=None)
        mocker.patch("services.auth_service.get_user_by_username", return_value=None)

        with pytest.raises(Exception, match="Password must be at least"):
            register_user("new@test.com", "newuser", "weak", "New", "User")


class TestLoginUser:
    def _make_user(self, email_verified=True):
        return {
            "id": 1,
            "email": "user@test.com",
            "username": "testuser",
            "password_hash": VALID_HASHED,
            "first_name": "Test",
            "last_name": "User",
            "email_verified": email_verified,
        }

    def test_success(self, mocker):
        mocker.patch("services.auth_service.get_user_by_username", return_value=self._make_user())
        mocker.patch("services.auth_service.generate_token", return_value="jwt-token")

        token, user_data = login_user("testuser", VALID_PASSWORD)
        assert token == "jwt-token"
        assert user_data["username"] == "testuser"

    def test_username_not_registered(self, mocker):
        mocker.patch("services.auth_service.get_user_by_username", return_value=None)

        with pytest.raises(Exception, match=ERR_USERNAME_NOT_REGISTERED):
            login_user("unknown", VALID_PASSWORD)

    def test_email_not_verified(self, mocker):
        mocker.patch("services.auth_service.get_user_by_username", return_value=self._make_user(email_verified=False))

        with pytest.raises(Exception, match=ERR_EMAIL_NOT_VERIFIED):
            login_user("testuser", VALID_PASSWORD)

    def test_invalid_password(self, mocker):
        mocker.patch("services.auth_service.get_user_by_username", return_value=self._make_user())

        with pytest.raises(Exception, match=ERR_INVALID_PASSWORD):
            login_user("testuser", "WrongP@ss1")


class TestVerifyEmailUser:
    def test_success(self, mocker):
        mocker.patch("services.auth_service.get_user_by_verification_token", return_value={"id": 1})
        mocker.patch("services.auth_service.confirm_user_email")

        verify_email_user("valid-token")

    def test_invalid_token(self, mocker):
        mocker.patch("services.auth_service.get_user_by_verification_token", return_value=None)

        with pytest.raises(Exception, match=ERR_INVALID_LINK):
            verify_email_user("bad-token")


class TestResetPasswordUser:
    def test_success(self, mocker):
        user = {"id": 1, "email": "user@test.com", "email_verified": True}
        mocker.patch("services.auth_service.get_user_by_email", return_value=user)
        mocker.patch("services.auth_service.set_token_reset_password_user_email")
        mocker.patch("services.auth_service.send_reset_password_email")

        reset_password_user("user@test.com")

    def test_email_not_registered(self, mocker):
        mocker.patch("services.auth_service.get_user_by_email", return_value=None)

        with pytest.raises(Exception, match=ERR_EMAIL_NOT_REGISTERED):
            reset_password_user("unknown@test.com")

    def test_email_not_verified(self, mocker):
        user = {"id": 1, "email": "user@test.com", "email_verified": False}
        mocker.patch("services.auth_service.get_user_by_email", return_value=user)

        with pytest.raises(Exception, match=ERR_EMAIL_NOT_VERIFIED):
            reset_password_user("user@test.com")


class TestVerifyResetPasswordUser:
    def test_success(self, mocker):
        mocker.patch("services.auth_service.set_new_password", return_value={"id": 1})

        verify_reset_password_user("valid-token", VALID_PASSWORD)

    def test_invalid_token(self, mocker):
        mocker.patch("services.auth_service.set_new_password", return_value=None)

        with pytest.raises(Exception, match=ERR_INVALID_LINK):
            verify_reset_password_user("bad-token", VALID_PASSWORD)
