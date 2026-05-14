import os
from models.profile_model import (
    create_profile, get_profile_by_user_id, update_profile,
    update_location, set_profile_complete
)
from models.user_model import get_user_by_id
from models.tag_model import get_user_tags, count_user_tags
from models.photo_model import get_photos_by_user, count_user_photos
from utils.profile_validator import (
    validate_gender, validate_sexual_preference,
    validate_biography, validate_birth_date,
    validate_location, validate_city
)
from services.constants import MIN_TAGS_FOR_COMPLETE, MIN_PHOTOS_FOR_COMPLETE
from services.errors import ERR_NO_FIELDS_TO_UPDATE

UPLOAD_BASE_URL = os.getenv("UPLOAD_BASE_URL", "http://localhost/uploads")

def get_public_profile_data(user_id):
    """Retourne les données publiques d'un profil pour la card Feed."""
    user = get_user_by_id(user_id)
    profile = get_profile_by_user_id(user_id)
    if not user or not profile:
        return None

    photos = get_photos_by_user(user_id)
    profile_photo = next((p["file_path"] for p in photos if p["is_profile"]), None)

    birth_date = profile.get("birth_date")

    return {
        "user_id": user_id,
        "first_name": user["first_name"],
        "birth_date": str(birth_date) if birth_date else None,
        "city": profile.get("city"),
        "profile_photo_url": (
            f"{UPLOAD_BASE_URL.rstrip('/')}/{profile_photo}"
            if profile_photo else None
        ),
    }


def get_or_create_profile(user_id):
    profile = get_profile_by_user_id(user_id)
    if not profile:
        profile = create_profile(user_id)
    return profile


def get_full_profile(user_id):
    profile = get_or_create_profile(user_id)
    user = get_user_by_id(user_id)
    tags = get_user_tags(user_id)
    photos = get_photos_by_user(user_id)

    profile["username"] = user["username"]
    profile["first_name"] = user["first_name"]
    profile["last_name"] = user["last_name"]
    profile["email"] = user["email"]
    profile["tags"] = tags
    profile["photos"] = photos

    return profile


FIELD_VALIDATORS = {
    "gender": validate_gender,
    "sexual_preference": validate_sexual_preference,
    "biography": validate_biography,
    "birth_date": validate_birth_date,
}


def update_user_profile(user_id, data):
    get_or_create_profile(user_id)

    fields_to_update = {}
    for field, validator in FIELD_VALIDATORS.items():
        if field in data:
            valid, error = validator(data[field])
            if not valid:
                raise Exception(error)
            fields_to_update[field] = data[field]

    if not fields_to_update:
        raise Exception(ERR_NO_FIELDS_TO_UPDATE)

    update_profile(user_id, fields_to_update)
    check_profile_completeness(user_id)

    return get_full_profile(user_id)


def update_user_location(user_id, lat, lng, city, consent):
    get_or_create_profile(user_id)

    valid, error = validate_location(lat, lng)
    if not valid:
        raise Exception(error)

    if city:
        valid, error = validate_city(city)
        if not valid:
            raise Exception(error)

    update_location(user_id, float(lat), float(lng), city, consent)


def check_profile_completeness(user_id):
    profile = get_profile_by_user_id(user_id)
    if not profile:
        return

    has_gender = profile.get("gender") is not None
    has_bio = profile.get("biography") is not None and len(str(profile["biography"]).strip()) > 0
    has_birth_date = profile.get("birth_date") is not None
    has_tags = count_user_tags(user_id) >= MIN_TAGS_FOR_COMPLETE
    has_photos = count_user_photos(user_id) >= MIN_PHOTOS_FOR_COMPLETE

    is_complete = has_gender and has_bio and has_birth_date and has_tags and has_photos
    set_profile_complete(user_id, is_complete)
