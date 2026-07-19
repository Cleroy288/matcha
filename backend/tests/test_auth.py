import uuid

import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

def test_register_login(client, mocker, monkeypatch):
    monkeypatch.setenv("DISABLE_EMAIL_VERIFICATION", "FALSE")
    mocker.patch("services.auth_service.send_verification_email")
    unique = uuid.uuid4().hex[:8]
    email = f"test_{unique}@test.com"
    username = f"user_{unique}"

    response = client.post("/register", json={
        "username": username,
        "email": email,
        "password": "Zxqv9!mN482",
        "confirm_password": "Zxqv9!mN482",
        "first_name": "Test",
        "last_name": "test"
    })
    assert response.status_code == 201
    assert response.get_json()["email_verification_required"] is True
    response = client.post("/login", json={
        "username": username,
        "password": "Zxqv9!mN482"
    })
    assert response.status_code == 400 #email not verified

def test_register_rejects_mismatched_passwords(client, mocker):
    create_user = mocker.patch("services.auth_service.create_user")

    response = client.post("/register", json={
        "username": "mismatch_user",
        "email": "mismatch@test.com",
        "password": "Zxqv9!mN482",
        "confirm_password": "Different9!Password",
        "first_name": "Test",
        "last_name": "User"
    })

    assert response.status_code == 400
    assert response.get_json()["error"] == "Passwords do not match"
    create_user.assert_not_called()

def test_register_reports_when_email_verification_is_disabled(client, mocker, monkeypatch):
    monkeypatch.setenv("DISABLE_EMAIL_VERIFICATION", "TRUE")
    mocker.patch("controllers.auth_controller.register_user")

    response = client.post("/register", json={
        "username": "onboarding_user",
        "email": "onboarding@test.com",
        "password": "Zxqv9!mN482",
        "confirm_password": "Zxqv9!mN482",
        "first_name": "Test",
        "last_name": "User"
    })

    assert response.status_code == 201
    assert response.get_json()["email_verification_required"] is False

def test_reset_password(client, mocker):
    mocker.patch("services.auth_service.send_reset_password_email")
    response = client.post("/reset-password", json={
        "email": "test@test.com"
    })
    assert response.status_code == 400

def test_me_unauthorized(client):
    response = client.get("/me")

    assert response.status_code in [401, 404]
