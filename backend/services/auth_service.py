import bcrypt
from models.user_model import create_user, get_user_by_email, get_user_by_username
from utils.auth_validator import validate_password, validate_email, validate_username
from services.jwt_service import generate_token

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

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    user_id = create_user(
        email,
        username,
        hashed.decode(),
        first_name,
        last_name
    )

    return user_id

def login_user(username, password):
    user =  get_user_by_username(username)
    if not user:	
        raise Exception("Username not registered")
    
    if not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        raise Exception("Invalid password")

    token = generate_token(user["id"])
    return token