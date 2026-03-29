import pytest
import uuid
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

def test_register_login(client, mocker):
    mocker.patch("services.auth_service.send_verification_email")
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

def test_reset_password(client, mocker):
    mocker.patch("services.auth_service.send_reset_password_email")
    response = client.post("/reset-password", json={
        "email": "test@test.com"
    })
    assert response.status_code == 400

def test_me_unauthorized(client):
    response = client.get("/me")

    assert response.status_code in [401, 404]
