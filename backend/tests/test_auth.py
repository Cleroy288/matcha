import pytest
import uuid
from unittest.mock import patch
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

@patch("services.auth_service.send_verification_email")
def test_register_login(mock_mail, client):
    unique = uuid.uuid4().hex[:8]
    email = f"test_{unique}@test.com"
    username = f"user_{unique}"
    
    response = client.post("/register", json={
        "username": username,
        "email": email,
        "password": "Password123*",
        "first_name": "Test",
        "last_name": "test"
    })
    assert response.status_code == 201
    response = client.post("/login", json={
        "username": username,
        "password": "Password123*"
    })
    assert response.status_code == 400 #email not verified

@patch("services.auth_service.send_reset_password_email")
def test_reset_password(mock_mail, client):
    response = client.post("/reset-password", json={
        "email": "test@test.com"
    })
    assert response.status_code in [200, 404]

def test_me_unauthorized(client):
    response = client.get("/me")

    assert response.status_code == 400
