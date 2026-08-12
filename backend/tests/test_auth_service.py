from services import auth_service


def test_login_exposes_profile_completion(monkeypatch):
    monkeypatch.setattr(auth_service, "get_user_by_username", lambda _username: {
        "id": 7,
        "username": "ada",
        "email": "ada@example.com",
        "password_hash": "hash",
        "first_name": "Ada",
        "last_name": "Lovelace",
        "email_verified": True,
        "profile_complete": False,
    })
    monkeypatch.setattr(auth_service.bcrypt, "checkpw", lambda _password, _hash: True)
    monkeypatch.setattr(auth_service, "generate_token", lambda _user_id: "token")

    token, user = auth_service.login_user("ada", "Password1!")

    assert token == "token"
    assert user["profile_complete"] is False
