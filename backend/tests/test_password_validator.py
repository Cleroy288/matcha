from utils.auth_validator import validate_password
from utils.constants import AuthMessages


def test_password_rejects_common_password_fragments():
    for password in ("Password123*", "P@ssw0rd123*", "Summer2026!"):
        valid, error = validate_password(password)

        assert valid is False
        assert error == AuthMessages.PASSWORD_TOO_COMMON


def test_password_accepts_non_dictionary_password():
    valid, error = validate_password("Zxqv9!mN482")

    assert valid is True
    assert error is None
