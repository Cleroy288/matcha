import os
import sys
import time

import jwt
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

os.environ["SECRET_KEY"] = "test-secret-key-for-pytest-32bytes!"
os.environ["JWT_EXP_DELTA_SECONDS"] = "3600"

from services.errors import ERR_INVALID_TOKEN, ERR_TOKEN_EXPIRED
from services.jwt_service import decode_token, generate_token


class TestGenerateToken:
    def test_returns_valid_jwt(self):
        token = generate_token(1)
        assert isinstance(token, str)
        payload = jwt.decode(token, "test-secret-key-for-pytest-32bytes!", algorithms=["HS256"])
        assert payload["user_id"] == 1

    def test_token_contains_expiration(self):
        token = generate_token(42)
        payload = jwt.decode(token, "test-secret-key-for-pytest-32bytes!", algorithms=["HS256"])
        assert "exp" in payload


class TestDecodeToken:
    def test_decode_valid_token(self):
        token = generate_token(1)
        payload = decode_token(token)
        assert payload["user_id"] == 1

    def test_decode_expired_token(self):
        expired_payload = {"user_id": 1, "exp": time.time() - 10}
        token = jwt.encode(expired_payload, "test-secret-key-for-pytest-32bytes!", algorithm="HS256")
        with pytest.raises(Exception, match=ERR_TOKEN_EXPIRED):
            decode_token(token)

    def test_decode_invalid_token(self):
        with pytest.raises(Exception, match=ERR_INVALID_TOKEN):
            decode_token("not-a-valid-token")

    def test_decode_wrong_signature(self):
        token = jwt.encode(
            {"user_id": 1, "exp": time.time() + 3600}, "wrong-secret-key-for-pytest-32bytes!", algorithm="HS256"
        )
        with pytest.raises(Exception, match=ERR_INVALID_TOKEN):
            decode_token(token)
