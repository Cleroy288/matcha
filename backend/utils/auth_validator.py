import re
from functools import lru_cache
from itertools import islice
from pathlib import Path

from utils.constants import COMMON_PASSWORDS, AuthMessages

EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)
PASSWORD_WORDLIST_MIN_LENGTH = 4
COMMON_ENGLISH_WORD_LIMIT = 2000
WORDLIST_DIR = Path(__file__).resolve().parents[1] / "data"
COMMON_PASSWORDS_FILE = WORDLIST_DIR / "10k-most-common-passwords.txt"
COMMON_ENGLISH_WORDS_FILE = WORDLIST_DIR / "google-10000-english.txt"
LEET_TRANSLATION = str.maketrans({
    "@": "a",
    "4": "a",
    "0": "o",
    "1": "i",
    "!": "i",
    "3": "e",
    "5": "s",
    "$": "s",
    "7": "t",
    "+": "t",
})
NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")

def validate_email(email):
    if len(email) > 254:
        return False
    return bool(EMAIL_REGEX.fullmatch(email))

def validate_username(username):
    if len(username) > 32:
        return False
    return True

def validate_password(password):
    if not isinstance(password, str):
        return False, AuthMessages.PASSWORD_INVALID

    if is_known_password(password):
        return False, AuthMessages.PASSWORD_TOO_COMMON

    if len(password) < 8:
        return False, AuthMessages.PASSWORD_INVALID_LEN

    if not re.search(r"[A-Z]", password):
        return False, AuthMessages.PASSWORD_INVALID_UP

    if not re.search(r"[0-9]", password):
        return False, AuthMessages.PASSWORD_INVALID_NUMBER

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, AuthMessages.PASSWORD_INVALID_SPECIAL

    return True, None


def is_known_password(password):
    normalized_password = normalize_password_text(password)
    return normalized_password in load_password_denylist()


def normalize_password_text(value):
    return NON_ALNUM_RE.sub("", value.lower().translate(LEET_TRANSLATION))


@lru_cache(maxsize=1)
def load_password_denylist():
    words = {normalize_password_text(word) for word in COMMON_PASSWORDS}
    words.update(load_wordlist(COMMON_PASSWORDS_FILE))
    words.update(load_wordlist(COMMON_ENGLISH_WORDS_FILE, limit=COMMON_ENGLISH_WORD_LIMIT))
    return {word for word in words if len(word) >= PASSWORD_WORDLIST_MIN_LENGTH}


def load_wordlist(path, limit=None):
    try:
        with path.open(encoding="utf-8", errors="ignore") as file:
            lines = file if limit is None else islice(file, limit)
            return {normalize_password_text(line.strip()) for line in lines}
    except FileNotFoundError:
        return set()
