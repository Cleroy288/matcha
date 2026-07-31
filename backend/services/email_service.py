import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

frontend_url = os.getenv("FRONTEND_URL")

def get_email_template(title, body_text, button_text, link):
    return f"""
    <html>
      <body style="background-color: #FDF6E3; padding: 20px; font-family: 'Arial', sans-serif;">
        <div style="max-width: 500px; margin: 0 auto; background-color: #BEF264; border: 3px solid #000000; box-shadow: 8px 8px 0px 0px #000000; padding: 40px; text-align: center;">
          <h1 style="font-family: 'Arial Black', sans-serif; text-transform: uppercase; color: #000; font-size: 28px; margin-bottom: 20px; letter-spacing: -1px;">
            {title}
          </h1>
          <p style="color: #000; font-size: 16px; line-height: 1.5; margin-bottom: 30px; font-weight: bold;">
            {body_text}
          </p>
          <a href="{link}" style="display: inline-block; background-color: #9717ff; color: #ffffff; border: 3px solid #000000; padding: 15px 30px; text-decoration: none; font-weight: bold; text-transform: uppercase; box-shadow: 4px 4px 0px 0px #000000; transition: 0.2s;">
            {button_text}
          </a>
          <p style="margin-top: 40px; font-size: 12px; color: #333;">
            If the button does not work, copy and paste this link: <br>
            <span style="word-break: break-all;">{link}</span>
          </p>
        </div>
      </body>
    </html>
    """

def send_verification_email(user_email, token):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    smtp_from = os.getenv("SMTP_FROM")


    verification_link = f"{frontend_url}/verify-email?token={token}"

    message = MIMEMultipart("alternative")
    message["From"] = smtp_from
    message["To"] = user_email
    message["Subject"] = "Matcha | Verify your account 🍵"

    html_content = get_email_template(
        "Welcome to Matcha",
        "Click the button below to confirm your registration and start matching.",
        "Verify my account",
        verification_link
    )
    message.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP(smtp_host, int(smtp_port)) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(message)
        return True
    except Exception:
        logger.exception("Failed to send verification email")
        return False

def send_reset_password_email(user_email, token):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    smtp_from = os.getenv("SMTP_FROM")

    verification_link = f"{frontend_url}/verify-reset-password?token={token}"

    message = MIMEMultipart("alternative")
    message["From"] = smtp_from
    message["To"] = user_email
    message["Subject"] = "Matcha | New password 🔑"

    html_content = get_email_template(
        "Reset your password",
        "You asked to change your password. Click the button below to set a new one.",
        "Change my password",
        verification_link
    )
    message.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP(smtp_host, int(smtp_port)) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(message)
        return True
    except Exception:
        logger.exception("Failed to send reset password email")
        return False