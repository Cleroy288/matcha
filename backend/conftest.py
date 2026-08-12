import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(__file__))
TEST_SECRET_KEY = "test-secret-key-for-pytest-32bytes!"
os.environ["SECRET_KEY"] = TEST_SECRET_KEY


@pytest.fixture()
def app():
    os.environ.setdefault("JWT_EXP_DELTA_SECONDS", "3600")
    os.environ.setdefault("POSTGRES_DB", "matcha_test")
    os.environ.setdefault("POSTGRES_USER", "test")
    os.environ.setdefault("POSTGRES_PASSWORD", "test")
    os.environ.setdefault("FRONTEND_URL", "http://localhost:5173")

    from app import app as flask_app

    flask_app.config["TESTING"] = True
    flask_app.config["SECRET_KEY"] = TEST_SECRET_KEY
    return flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def auth_headers():
    def _headers(token):
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    return _headers


@pytest.fixture()
def fake_user():
    return {
        "id": 1,
        "email": "test@example.com",
        "username": "testuser",
        "password_hash": "$2b$12$LJ3m4ys3Lk0TSwHjbJ4oruL9Gvj5cGmmNqKOcG3HMqBbCXfOH0Pey",
        "first_name": "Test",
        "last_name": "User",
        "email_verified": True,
    }


@pytest.fixture()
def fake_profile():
    return {
        "id": 1,
        "user_id": 1,
        "gender": "male",
        "sexual_preference": "bisexual",
        "biography": "Hello world",
        "birth_date": "2000-01-01",
        "fame_rating": 0,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "city": "Paris",
        "gps_consent": True,
        "last_online": None,
        "is_online": False,
        "profile_complete": False,
        "created_at": None,
        "updated_at": None,
    }
