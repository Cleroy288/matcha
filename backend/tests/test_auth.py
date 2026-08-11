from utils.constants import AuthMessages

PASSWORD = "Zxqv9!mN482"
REGISTER_BODY = {
    "username": "new_user",
    "email": "new_user@test.com",
    "password": PASSWORD,
    "confirm_password": PASSWORD,
    "first_name": "Test",
    "last_name": "test",
}


def fake_user_store(mocker):
    """In-memory stand-in for the users table: register really hashes the password
    and login really reads it back, so the business rules stay under test."""
    stored = {}

    def create_user(email, username, password_hash, first_name, last_name, _token, email_verified):
        stored.update({
            "id": 7,
            "email": email,
            "username": username,
            "password_hash": password_hash,
            "first_name": first_name,
            "last_name": last_name,
            "email_verified": email_verified,
            "profile_complete": False,
        })
        return stored["id"]

    mocker.patch("services.auth_service.get_user_by_email", return_value=None)
    mocker.patch("services.auth_service.get_user_by_username", side_effect=lambda _u: stored or None)
    mocker.patch("services.auth_service.create_user", side_effect=create_user)
    return stored


def test_register_then_login_is_refused_until_the_email_is_verified(client, mocker, monkeypatch):
    monkeypatch.setenv("DISABLE_EMAIL_VERIFICATION", "FALSE")
    fake_user_store(mocker)
    send_verification_email = mocker.patch("services.auth_service.send_verification_email")

    response = client.post("/register", json=REGISTER_BODY)

    assert response.status_code == 201
    assert response.get_json()["email_verification_required"] is True
    send_verification_email.assert_called_once()

    response = client.post("/login", json={"username": "new_user", "password": PASSWORD})

    assert response.status_code == 400
    assert response.get_json()["error"] == AuthMessages.EMAIL_NOT_VERIFIED


def test_login_after_verification_returns_the_user_contract(client, mocker, monkeypatch):
    monkeypatch.setenv("DISABLE_EMAIL_VERIFICATION", "TRUE")
    fake_user_store(mocker)

    assert client.post("/register", json=REGISTER_BODY).status_code == 201

    response = client.post("/login", json={"username": "new_user", "password": PASSWORD})

    assert response.status_code == 200
    assert response.get_json()["user"] == {
        "id": 7,
        "username": "new_user",
        "email": "new_user@test.com",
        "first_name": "Test",
        "last_name": "test",
        "profile_complete": False,
    }


def test_login_rejects_a_wrong_password(client, mocker, monkeypatch):
    monkeypatch.setenv("DISABLE_EMAIL_VERIFICATION", "TRUE")
    fake_user_store(mocker)
    client.post("/register", json=REGISTER_BODY)

    response = client.post("/login", json={"username": "new_user", "password": "Wrong9!Password"})

    assert response.status_code == 400
    assert response.get_json()["error"] == AuthMessages.PASSWORD_INVALID

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

def test_reset_password_stores_the_token_it_emails(client, mocker):
    mocker.patch("services.auth_service.get_user_by_email", return_value={"id": 7, "email_verified": True})
    store_token = mocker.patch("services.auth_service.set_token_reset_password_user_email")
    send_email = mocker.patch("services.auth_service.send_reset_password_email")

    response = client.post("/reset-password", json={"email": "test@test.com"})

    assert response.status_code == 200
    # the emailed token is worthless unless the exact same one is persisted
    assert store_token.call_args.args == send_email.call_args.args
    assert store_token.call_args.args[0] == "test@test.com"


def test_reset_password_refuses_an_unverified_email(client, mocker):
    mocker.patch("services.auth_service.get_user_by_email", return_value={"id": 7, "email_verified": False})
    send_email = mocker.patch("services.auth_service.send_reset_password_email")

    response = client.post("/reset-password", json={"email": "test@test.com"})

    assert response.status_code == 400
    assert response.get_json()["error"] == AuthMessages.EMAIL_NOT_VERIFIED
    send_email.assert_not_called()

def test_me_unauthorized(client):
    response = client.get("/me")

    assert response.status_code in [401, 404]
