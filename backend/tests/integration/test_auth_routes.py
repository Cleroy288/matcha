import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest-32bytes!")
os.environ.setdefault("JWT_EXP_DELTA_SECONDS", "3600")
os.environ.setdefault("FRONTEND_URL", "http://localhost:5173")

from controllers.errors import ERR_MISSING_TOKEN


@pytest.fixture()
def app():
    from flask import Flask

    from routes.auth_routes import auth_routes

    test_app = Flask(__name__)
    test_app.config["TESTING"] = True
    test_app.config["SECRET_KEY"] = "test-secret-key-for-pytest-32bytes!"
    test_app.register_blueprint(auth_routes)
    return test_app


@pytest.fixture()
def client(app):
    return app.test_client()


class TestRegisterRoute:
    def test_success(self, client, mocker):
        mocker.patch("controllers.auth_controller.register_user", return_value=1)

        response = client.post(
            "/register",
            json={
                "email": "new@test.com",
                "username": "newuser",
                "password": "StrongP@ss1",
                "first_name": "New",
                "last_name": "User",
            },
        )
        data = json.loads(response.data)
        assert response.status_code == 201
        assert data["user_id"] == 1

    def test_error(self, client, mocker):
        mocker.patch("controllers.auth_controller.register_user", side_effect=Exception("Email already registered"))

        response = client.post(
            "/register",
            json={
                "email": "taken@test.com",
                "username": "newuser",
                "password": "StrongP@ss1",
                "first_name": "New",
                "last_name": "User",
            },
        )
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "error" in data


class TestLoginRoute:
    def test_success(self, client, mocker):
        user_data = {"id": 1, "username": "testuser", "email": "test@test.com", "first_name": "T", "last_name": "U"}
        mocker.patch("controllers.auth_controller.login_user", return_value=("jwt-token", user_data))

        response = client.post("/login", json={"username": "testuser", "password": "StrongP@ss1"})
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data["token"] == "jwt-token"
        assert data["user"]["username"] == "testuser"

    def test_error(self, client, mocker):
        mocker.patch("controllers.auth_controller.login_user", side_effect=Exception("Invalid password"))

        response = client.post("/login", json={"username": "testuser", "password": "wrong"})
        assert response.status_code == 400


class TestVerifyEmailRoute:
    def test_success(self, client, mocker):
        mocker.patch("controllers.auth_controller.verify_email_user")

        response = client.get("/verify-email?token=valid-token")
        data = json.loads(response.data)
        assert response.status_code == 200
        assert "message" in data

    def test_missing_token(self, client):
        response = client.get("/verify-email")
        data = json.loads(response.data)
        assert response.status_code == 400
        assert data["error"] == ERR_MISSING_TOKEN


class TestResetPasswordRoute:
    def test_success(self, client, mocker):
        mocker.patch("controllers.auth_controller.reset_password_user")

        response = client.post("/reset-password", json={"email": "user@test.com"})
        data = json.loads(response.data)
        assert response.status_code == 200
        assert "message" in data

    def test_error(self, client, mocker):
        mocker.patch("controllers.auth_controller.reset_password_user", side_effect=Exception("Email not registered"))

        response = client.post("/reset-password", json={"email": "unknown@test.com"})
        assert response.status_code == 400


class TestVerifyResetPasswordRoute:
    def test_success(self, client, mocker):
        mocker.patch("controllers.auth_controller.verify_reset_password_user")

        response = client.post("/verify-reset-password?token=valid-token", json={"password": "NewP@ss1"})
        data = json.loads(response.data)
        assert response.status_code == 200
        assert "message" in data

    def test_missing_token(self, client):
        response = client.post("/verify-reset-password", json={"password": "NewP@ss1"})
        data = json.loads(response.data)
        assert response.status_code == 400
        assert data["error"] == ERR_MISSING_TOKEN


class TestMeRoute:
    def test_success(self, client, mocker):
        mocker.patch("utils.jwt_required.decode_token", return_value={"user_id": 1})
        mocker.patch(
            "controllers.auth_controller.get_user_by_id",
            return_value={"id": 1, "username": "testuser", "email": "test@test.com"},
        )

        response = client.get("/me", headers={"Authorization": "Bearer valid-token"})
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data["user"]["username"] == "testuser"

    def test_no_token(self, client):
        response = client.get("/me")
        assert response.status_code == 401
