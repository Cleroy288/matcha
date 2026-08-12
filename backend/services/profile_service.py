from datetime import date

from models.block_model import is_blocked
from models.like_model import has_liked, is_match
from models.photo_model import get_photos_by_user
from models.profile_model import (
    create_profile,
    get_profile_by_user_id,
    set_profile_complete,
    update_location,
    update_profile,
)
from models.tag_model import count_user_tags, get_user_tags
from models.user_model import get_user_by_email, get_user_by_id, update_user
from services.constants import MIN_PHOTOS_FOR_COMPLETE, MIN_TAGS_FOR_COMPLETE
from services.errors import ERR_INVALID_NAME, ERR_NO_FIELDS_TO_UPDATE
from utils.auth_validator import validate_email
from utils.constants import AuthMessages
from utils.geo import haversine_km
from utils.photo_url import build_photo_url
from utils.profile_validator import (
    validate_biography,
    validate_birth_date,
    validate_city,
    validate_gender,
    validate_location,
    validate_sexual_preference,
)


def get_public_profile_data(viewer_id, user_id):
    """Profile view: every public field (never email/password), distance,
    online status and relation with the viewer (like / match / block)."""
    user = get_user_by_id(user_id)
    profile = get_profile_by_user_id(user_id)
    # 1 missing profile, or blocked either way → invisible
    if not user or not profile:
        return None
    if viewer_id != user_id and is_blocked(viewer_id, user_id):
        return None

    public = build_public_fields(user, profile)
    public["photos"] = build_photo_list(user_id)
    public["profile_photo_url"] = find_profile_photo_url(public["photos"])
    public["tags"] = get_user_tags(user_id)
    public["distance_km"] = compute_viewer_distance(viewer_id, profile)
    public.update(build_relation_fields(viewer_id, user_id))
    return public


def build_public_fields(user, profile):
    """Public profile fields; email and password excluded (subject IV.5)."""
    birth_date = profile.get("birth_date")
    return {
        "user_id": user["id"],
        "username": user["username"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "gender": profile.get("gender"),
        "sexual_preference": profile.get("sexual_preference"),
        "biography": profile.get("biography"),
        "birth_date": str(birth_date) if birth_date else None,
        "age": compute_age(birth_date),
        "city": profile.get("city"),
        "fame_rating": float(profile.get("fame_rating") or 0),
        "is_online": profile.get("is_online"),
        "last_online": profile.get("last_online"),
    }


def build_photo_list(user_id):
    """Profile photos with their public URL served by nginx."""
    photos = get_photos_by_user(user_id)
    for photo in photos:
        photo["url"] = build_photo_url(photo["file_path"])
    return photos


def find_profile_photo_url(photos):
    # a profile without a profile photo is a legitimate case → None
    return next((p["url"] for p in photos if p["is_profile"]), None)


def compute_viewer_distance(viewer_id, profile):
    """Distance viewer → viewed profile; None when a position is missing."""
    viewer_profile = get_profile_by_user_id(viewer_id)
    if not viewer_profile:
        return None
    return haversine_km(
        viewer_profile.get("latitude"), viewer_profile.get("longitude"),
        profile.get("latitude"), profile.get("longitude")
    )


def build_relation_fields(viewer_id, user_id):
    """Relation between the viewer and the profile: liked, likes me, connected (subject IV.5)."""
    if viewer_id == user_id:
        return {"liked_by_me": False, "likes_me": False, "connected": False}
    return {
        "liked_by_me": has_liked(viewer_id, user_id),
        "likes_me": has_liked(user_id, viewer_id),
        "connected": is_match(viewer_id, user_id),
    }


def compute_age(birth_date):
    # no birth date means an incomplete profile → unknown age
    if not birth_date:
        return None
    today = date.today()
    before_birthday = (today.month, today.day) < (birth_date.month, birth_date.day)
    return today.year - birth_date.year - before_birthday


def get_or_create_profile(user_id):
    profile = get_profile_by_user_id(user_id)
    if not profile:
        profile = create_profile(user_id)
    return profile


def get_full_profile(user_id):
    get_or_create_profile(user_id)
    check_profile_completeness(user_id)
    profile = get_profile_by_user_id(user_id)
    user = get_user_by_id(user_id)
    tags = get_user_tags(user_id)
    photos = get_photos_by_user(user_id)

    profile["username"] = user["username"]
    profile["first_name"] = user["first_name"]
    profile["last_name"] = user["last_name"]
    profile["email"] = user["email"]
    profile["birth_date"] = str(profile["birth_date"]) if profile.get("birth_date") else None
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

    if not isinstance(data, dict):
        raise Exception(ERR_NO_FIELDS_TO_UPDATE)

    profile_fields = {}
    for field, validator in FIELD_VALIDATORS.items():
        if field in data:
            valid, error = validator(data[field])
            if not valid:
                raise Exception(error)
            profile_fields[field] = data[field]

    user_fields = {}
    for field in ("first_name", "last_name"):
        if field in data:
            value = data[field]
            if not isinstance(value, str) or not 1 <= len(value.strip()) <= 100:
                raise Exception(ERR_INVALID_NAME)
            user_fields[field] = value.strip()

    if "email" in data:
        email = data["email"]
        if not isinstance(email, str) or not validate_email(email.strip()):
            raise Exception(AuthMessages.INVALID_EMAIL_FORMAT)
        email = email.strip()
        existing_user = get_user_by_email(email)
        if existing_user and existing_user["id"] != user_id:
            raise Exception(AuthMessages.EMAIL_ALREADY_EXISTS)
        user_fields["email"] = email

    if not profile_fields and not user_fields:
        raise Exception(ERR_NO_FIELDS_TO_UPDATE)

    if user_fields:
        update_user(user_id, user_fields)
    if profile_fields:
        update_profile(user_id, profile_fields)
    check_profile_completeness(user_id)

    return get_full_profile(user_id)


def update_user_location(user_id, lat, lng, city, consent):
    get_or_create_profile(user_id)

    city = city.strip() if isinstance(city, str) else ""
    if consent is True:
        valid, error = validate_location(lat, lng)
        if not valid:
            raise Exception(error)
        latitude, longitude = float(lat), float(lng)
    else:
        valid, error = validate_city(city)
        if not valid:
            raise Exception(error)
        latitude, longitude = None, None

    if city:
        valid, error = validate_city(city)
        if not valid:
            raise Exception(error)

    update_location(user_id, latitude, longitude, city, consent is True)
    check_profile_completeness(user_id)


def check_profile_completeness(user_id):
    profile = get_profile_by_user_id(user_id)
    if not profile:
        return

    has_gender = profile.get("gender") is not None
    has_preference = profile.get("sexual_preference") is not None
    has_bio = profile.get("biography") is not None and len(str(profile["biography"]).strip()) > 0
    has_birth_date = profile.get("birth_date") is not None
    has_tags = count_user_tags(user_id) >= MIN_TAGS_FOR_COMPLETE
    photos = get_photos_by_user(user_id)
    has_photos = len(photos) >= MIN_PHOTOS_FOR_COMPLETE
    has_profile_photo = any(photo.get("is_profile") for photo in photos)
    has_location = (
        profile.get("gps_consent") is True
        and profile.get("latitude") is not None
        and profile.get("longitude") is not None
    ) or bool(str(profile.get("city") or "").strip())

    is_complete = (
        has_gender
        and has_preference
        and has_bio
        and has_birth_date
        and has_tags
        and has_photos
        and has_profile_photo
        and has_location
    )
    if profile.get("profile_complete") != is_complete:
        set_profile_complete(user_id, is_complete)
