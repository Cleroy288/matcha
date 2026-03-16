import os
from models.photo_model import (
    create_photo, get_photos_by_user, get_photo_by_id,
    count_user_photos, delete_photo, set_profile_photo
)
from utils.upload_validator import (
    validate_image_file, validate_image_mime,
    validate_image_size, generate_safe_filename
)
from services.profile_service import check_profile_completeness
from services.constants import MAX_PHOTOS, UPLOAD_DIR
from services.errors import ERR_MAX_PHOTOS, ERR_PHOTO_NOT_FOUND, ERR_NOT_AUTHORIZED


def upload_photo(user_id, file_storage):
    photo_count = count_user_photos(user_id)
    if photo_count >= MAX_PHOTOS:
        raise Exception(ERR_MAX_PHOTOS)

    valid, error = validate_image_file(file_storage)
    if not valid:
        raise Exception(error)

    valid, error = validate_image_mime(file_storage)
    if not valid:
        raise Exception(error)

    valid, error = validate_image_size(file_storage)
    if not valid:
        raise Exception(error)

    filename = generate_safe_filename(file_storage.filename)
    save_path = os.path.join(UPLOAD_DIR, filename)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_storage.save(save_path)

    is_first_photo = photo_count == 0
    try:
        photo = create_photo(user_id, filename, is_first_photo, photo_count)
    except Exception:
        if os.path.exists(save_path):
            os.remove(save_path)
        raise

    check_profile_completeness(user_id)
    return photo


def delete_user_photo(user_id, photo_id):
    photo = get_photo_by_id(photo_id)
    if not photo:
        raise Exception(ERR_PHOTO_NOT_FOUND)
    if photo["user_id"] != user_id:
        raise Exception(ERR_NOT_AUTHORIZED)

    was_profile = photo["is_profile"]
    result = delete_photo(photo_id)

    if result:
        file_path = os.path.join(UPLOAD_DIR, result["file_path"])
        if os.path.exists(file_path):
            os.remove(file_path)

    if was_profile:
        remaining = get_photos_by_user(user_id)
        if remaining:
            set_profile_photo(user_id, remaining[0]["id"])

    check_profile_completeness(user_id)


def set_user_profile_photo(user_id, photo_id):
    photo = get_photo_by_id(photo_id)
    if not photo:
        raise Exception(ERR_PHOTO_NOT_FOUND)
    if photo["user_id"] != user_id:
        raise Exception(ERR_NOT_AUTHORIZED)

    set_profile_photo(user_id, photo_id)


def get_user_photos(user_id):
    return get_photos_by_user(user_id)
