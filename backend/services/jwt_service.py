import os
import jwt
from datetime import UTC, datetime, timedelta
from dotenv import load_dotenv
from services.errors import ERR_TOKEN_EXPIRED, ERR_INVALID_TOKEN
from services.constants import JWT_EXP_DEFAULT

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
EXP_DELTA_SECONDS = int(os.getenv("JWT_EXP_DELTA_SECONDS", JWT_EXP_DEFAULT))


def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(UTC) + timedelta(seconds=EXP_DELTA_SECONDS)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception(ERR_TOKEN_EXPIRED)
    except jwt.InvalidTokenError:
        raise Exception(ERR_INVALID_TOKEN)
