import os
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv

from utils.constants import AuthMessages

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
EXP_DELTA_SECONDS = int(os.getenv("JWT_EXP_DELTA_SECONDS", 3600))


def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(seconds=EXP_DELTA_SECONDS)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception(AuthMessages.TOKEN_EXPIRED) from None
    except jwt.InvalidTokenError:
        raise Exception(AuthMessages.INVALID_TOKEN) from None
