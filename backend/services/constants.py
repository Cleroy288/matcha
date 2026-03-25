import os
from dotenv import load_dotenv

load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

MAX_TAGS_PER_USER = 10
MAX_PHOTOS = 5
MIN_TAGS_FOR_COMPLETE = 1
MIN_PHOTOS_FOR_COMPLETE = 1
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
TAG_SEARCH_LIMIT = 20
JWT_EXP_DEFAULT = 3600
