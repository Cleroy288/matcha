import re

class AuthMessages:
    EMAIL_VERIFIED        = "Email vérifié avec succès ! Tu peux maintenant te connecter."
    EMAIL_SEND_SUCCESS    = "Email envoyé avec succès ! Tu peux maintenant clic sur le lien dans ton mail pour changer de mot de passe."
    INVALID_EMAIL_FORMAT  = "Format de l'email invalide"
    NOT_EMAIL             = "Email manquante"
    EMAIL_NOT_VERIFIED    = "Email non vérifié"
    EMAIL_ALREADY_EXISTS   = "Cet email est déjà pris."

    PASSWORD_RESET_OK     = "Mot de passe modifié avec succès ! Tu peux maintenant te connecter."
    PASSWORD_INVALID      = "Mot de passe invalide"
    PASSWORD_INVALID_LEN  = "Le mot de passe doit contenir au moins 8 caractères"
    PASSWORD_INVALID_UP  = "Le mot de passe doit contenir au moins 1 majuscule"
    PASSWORD_INVALID_NUMBER  = "Le mot de passe doit contenir au moins 1 chiffre"
    PASSWORD_INVALID_SPECIAL  = "Le mot de passe doit contenir au moins 1 caractère spéciale"

    NOT_TOKEN             = "Token manquant"
    INVALID_TOKEN         = "Token invalide"
    TOKEN_EXPIRED         = "Token expiré"
    USER_NOT_FOUND        = "Utilisateur introuvable"
    USERNAME_ALREADY_EXISTS   = "Ce nom d'utilisateur est déjà pris."
    USERNAME_NOT_VALID    = "Nom d'utilisateur limité à 32 caractères"

    REGISTER_SUCCES       = "Enregistré avec succès. Tu dois maintenant valider ton email pour te connecter"
    LOGIN_SUCCESS         = "Connecté avec succès."




VALID_GENDERS = {"male", "female", "other"}
VALID_PREFERENCES = {"male", "female", "bisexual"}
TAG_REGEX = re.compile(r"^#[a-zA-Z0-9-]+$")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

COMMON_PASSWORDS = {
    "password", "password123", "123456", "qwerty", "letmein"
}

EMAIL_MAX_LENGTH = 254
USERNAME_MAX_LENGTH = 32
PASSWORD_MIN_LENGTH = 8

BIO_MIN_LENGTH = 1
BIO_MAX_LENGTH = 500

MIN_AGE = 18
MAX_AGE = 120

TAG_NAME_MAX_LENGTH = 50

LATITUDE_MIN = -90
LATITUDE_MAX = 90
LONGITUDE_MIN = -180
LONGITUDE_MAX = 180

CITY_MIN_LENGTH = 1
CITY_MAX_LENGTH = 100

ALLOWED_IMAGE_FORMATS = {"JPEG", "PNG", "WEBP"}
MAX_FILE_SIZE = 5 * 1024 * 1024
DEFAULT_IMAGE_EXTENSION = ".jpg"
