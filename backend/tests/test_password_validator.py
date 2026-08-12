from utils.auth_validator import validate_password
from utils.constants import AuthMessages


def test_password_rejects_known_passwords_but_accepts_distinct_ones():
    for password in ("Password123*", "P@ssw0rd123*"):
        valid, error = validate_password(password)

        assert valid is False
        assert error == AuthMessages.PASSWORD_TOO_COMMON

    valid, error = validate_password("Summer2026!")

    assert valid is True
    assert error is None


def test_password_accepts_non_dictionary_password():
    valid, error = validate_password("Zxqv9!mN482")

    assert valid is True
    assert error is None
