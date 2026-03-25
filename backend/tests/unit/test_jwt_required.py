import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest-32bytes!")

from services.errors import ERR_TOKEN_EXPIRED
from utils.errors import ERR_TOKEN_MISSING
from utils.jwt_required import jwt_required


@pytest.fixture()
def app():
    from flask import Flask

    test_app = Flask(__name__)
    test_app.config["TESTING"] = True

    @test_app.route("/protected")
    @jwt_required
    def protected(payload):
        return {"user_id": payload["user_id"]}

    return test_app


@pytest.fixture()
def client(app):
    return app.test_client()


class TestJwtRequired:
    def test_valid_token(self, client, mocker):
        mocker.patch("utils.jwt_required.decode_token", return_value={"user_id": 1})

        response = client.get("/protected", headers={"Authorization": "Bearer valid-token"})
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data["user_id"] == 1

    def test_no_auth_header(self, client):
        response = client.get("/protected")
        data = json.loads(response.data)
        assert response.status_code == 401
        assert data["error"] == ERR_TOKEN_MISSING

    def test_malformed_header(self, client):
        response = client.get("/protected", headers={"Authorization": "NotBearer token"})
        data = json.loads(response.data)
        assert response.status_code == 401
        assert data["error"] == ERR_TOKEN_MISSING

    def test_expired_token(self, client, mocker):
        mocker.patch("utils.jwt_required.decode_token", side_effect=Exception(ERR_TOKEN_EXPIRED))

        response = client.get("/protected", headers={"Authorization": "Bearer expired-token"})
        data = json.loads(response.data)
        assert response.status_code == 401
        assert ERR_TOKEN_EXPIRED in data["error"]
