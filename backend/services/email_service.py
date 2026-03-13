import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
            Si le bouton ne fonctionne pas, copie-colle ceci : <br>
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

    # Le lien qui pointe vers ton FRONTEND (Vite)
    verification_link = f"http://localhost:5173/verify-email?token={token}"

    message = MIMEMultipart("alternative")
    message["From"] = smtp_from
    message["To"] = user_email
    message["Subject"] = "Matcha | Vérifie ton compte ! 🍵"

    html_content = get_email_template(
        "Bienvenue sur Matcha",
        "Clique sur le bouton ci-dessous pour valider ton inscription et commencer à matcher !",
        "Vérifier mon compte",
        verification_link
    )
    message.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP(smtp_host, int(smtp_port)) as server:
            server.starttls() # Sécurise la connexion
            server.login(smtp_user, smtp_pass)
            server.send_message(message)
        return True
    except Exception as e:
        print(f"Erreur envoi mail: {e}")
        return False
    
def send_reset_password_email(user_email, token):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    smtp_from = os.getenv("SMTP_FROM")

    # Le lien qui pointe vers ton FRONTEND (Vite)
    verification_link = f"http://localhost:5173/verify-reset-password?token={token}"

    message = MIMEMultipart("alternative")
    message["From"] = smtp_from
    message["To"] = user_email
    message["Subject"] = "Matcha | Nouveau mot de passe 🔑"

    html_content = get_email_template(
        "Reset Password",
        "Tu as demandé à changer ton mot de passe. Clique sur le bouton ci-dessous pour le modifier en toute sécurité.",
        "Changer mon mot de passe",
        verification_link
    )
    message.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP(smtp_host, int(smtp_port)) as server:
            server.starttls() # Sécurise la connexion
            server.login(smtp_user, smtp_pass)
            server.send_message(message)
        return True
    except Exception as e:
        print(f"Erreur envoi mail: {e}")
        return False