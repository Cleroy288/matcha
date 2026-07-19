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

# paramètres de l'algo de suggestions (score = tags communs + proximité + fame)
SUGGESTION_WEIGHT_COMMON_TAG = 10        # points par tag partagé
SUGGESTION_WEIGHT_FAME = 2               # points par point de fame (0-10)
SUGGESTION_WEIGHT_SAME_CITY = 1000        # priorité aux profils de la même ville
SUGGESTION_PROXIMITY_RADIUS_KM = 100     # au-delà, plus aucun point de proximité
SUGGESTION_PROXIMITY_POINTS_PER_KM = 0.5 # 50 pts à 0 km, 0 pt à 100 km
SUGGESTION_FAR_DISTANCE_KM = 20000       # distance attribuée aux profils sans position

# pagination navigation / recherche
BROWSE_DEFAULT_LIMIT = 50
BROWSE_MAX_LIMIT = 200

# chat
MESSAGE_MAX_LENGTH = 1000
CONVERSATION_MESSAGES_LIMIT = 100
