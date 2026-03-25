import os
import sys
from unittest.mock import MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

os.environ.setdefault("SMTP_HOST", "smtp.test.com")
os.environ.setdefault("SMTP_PORT", "587")
os.environ.setdefault("SMTP_USER", "testuser")
os.environ.setdefault("SMTP_PASS", "testpass")
os.environ.setdefault("SMTP_FROM", "noreply@test.com")
os.environ.setdefault("FRONTEND_URL", "http://localhost:5173")

from services.email_service import get_email_template, send_reset_password_email, send_verification_email


class TestGetEmailTemplate:
    def test_returns_html_with_content(self):
        html = get_email_template("Title", "Body text", "Click me", "https://example.com")
        assert "Title" in html
        assert "Body text" in html
        assert "Click me" in html
        assert "https://example.com" in html
        assert "<html>" in html


class TestSendVerificationEmail:
    def test_success(self, mocker):
        mock_smtp_instance = MagicMock()
        mock_smtp_class = mocker.patch("services.email_service.smtplib.SMTP")
        mock_smtp_class.return_value.__enter__ = MagicMock(return_value=mock_smtp_instance)
        mock_smtp_class.return_value.__exit__ = MagicMock(return_value=False)

        result = send_verification_email("user@test.com", "abc123token")
        assert result is True

    def test_smtp_failure(self, mocker):
        mock_smtp_class = mocker.patch("services.email_service.smtplib.SMTP")
        mock_smtp_class.side_effect = Exception("SMTP connection failed")

        result = send_verification_email("user@test.com", "abc123token")
        assert result is False


class TestSendResetPasswordEmail:
    def test_success(self, mocker):
        mock_smtp_instance = MagicMock()
        mock_smtp_class = mocker.patch("services.email_service.smtplib.SMTP")
        mock_smtp_class.return_value.__enter__ = MagicMock(return_value=mock_smtp_instance)
        mock_smtp_class.return_value.__exit__ = MagicMock(return_value=False)

        result = send_reset_password_email("user@test.com", "resettoken123")
        assert result is True

    def test_smtp_failure(self, mocker):
        mock_smtp_class = mocker.patch("services.email_service.smtplib.SMTP")
        mock_smtp_class.side_effect = Exception("SMTP connection failed")

        result = send_reset_password_email("user@test.com", "resettoken123")
        assert result is False
