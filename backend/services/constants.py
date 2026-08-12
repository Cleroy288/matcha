import os

from dotenv import load_dotenv

load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

MAX_TAGS_PER_USER = 10
MAX_PHOTOS = 5
MIN_TAGS_FOR_COMPLETE = 5
MIN_PHOTOS_FOR_COMPLETE = 1
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
TAG_SEARCH_LIMIT = 20
JWT_EXP_DEFAULT = 3600

# suggestion algorithm parameters (score = common tags + proximity + fame)
SUGGESTION_WEIGHT_COMMON_TAG = 10        # points per shared tag
SUGGESTION_WEIGHT_FAME = 2               # points per fame point (0-10)
SUGGESTION_WEIGHT_SAME_CITY = 1000        # priority to profiles in the same city
SUGGESTION_PROXIMITY_RADIUS_KM = 100     # beyond this, no proximity point at all
SUGGESTION_PROXIMITY_POINTS_PER_KM = 0.5 # 50 pts at 0 km, 0 pt at 100 km
SUGGESTION_FAR_DISTANCE_KM = 20000       # distance assigned to profiles without a position

# pagination navigation / recherche
BROWSE_DEFAULT_LIMIT = 50
BROWSE_MAX_LIMIT = 200

# chat
MESSAGE_MAX_LENGTH = 1000
CONVERSATION_MESSAGES_LIMIT = 100
