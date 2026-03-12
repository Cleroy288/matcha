import bcrypt
import secrets
from models.user_model import create_user, get_user_by_email, get_user_by_username, set_token_reset_password_user_email, get_user_by_verification_token, set_new_password, confirm_user_email
from utils.auth_validator import validate_password, validate_email, validate_username
from services.jwt_service import generate_token
from services.email_service import send_verification_email, send_reset_password_email

def register_user(email, username, password, first_name, last_name):

    if validate_email(email) is False:
        raise Exception("Invalid email format")
    if validate_username(username) is False:
        raise Exception("Username limited to 32 characters")

    user_email =  get_user_by_email(email)
    if user_email:	
        raise Exception("Email already registered")

    user_username =  get_user_by_username(username)
    if user_username:	
        raise Exception("Username already taken")
        
    valid, error = validate_password(password)

    if not valid:
        raise Exception(error)
    
    verification_token = secrets.token_urlsafe(32)

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    user_id = create_user(
        email,
        username,
        hashed.decode(),
        first_name,
        last_name,
        verification_token
    )

    send_verification_email(email, verification_token)

    return user_id


def login_user(username, password):
    user =  get_user_by_username(username)
    if not user:	
        raise Exception("Username not registered")

    
    if not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        raise Exception("Invalid password")
    if not user["email_verified"]:
        raise Exception("Email is not verified")
    
    token = generate_token(user["id"])

    user_data = {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "first_name": user["first_name"],
        "last_name": user["last_name"]
    }

    return token, user_data


def verify_email_user(token):
    user = get_user_by_verification_token(token)
    if not user:
        raise Exception("Lien invalide ou expiré")

    confirm_user_email(user['id'])


def reset_password_user(email):

    if validate_email(email) is False:
        raise Exception("Invalid email format")
    user =  get_user_by_email(email)
    if not user:	
        raise Exception("Email not registered")
    if not user["email_verified"]:
        raise Exception("Email not verified")
    
    verification_token = secrets.token_urlsafe(32)
    set_token_reset_password_user_email(email, verification_token)
    send_reset_password_email(email, verification_token)


def verify_reset_password_user(token, password):
        valid, error = validate_password(password)
        if not valid:
            raise Exception(error)
    
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        user = set_new_password(hashed.decode(), token)
        if not user:
            raise Exception("Lien invalide ou expiré")
