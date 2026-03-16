import uuid
import os
from PIL import Image
from utils.constants import ALLOWED_IMAGE_FORMATS, MAX_FILE_SIZE, DEFAULT_IMAGE_EXTENSION
from utils.errors import ERR_NO_FILE, ERR_INVALID_IMAGE, ERR_INVALID_IMAGE_FORMAT, ERR_IMAGE_TOO_LARGE


def validate_image_file(file_storage):
    if not file_storage or file_storage.filename == "":
        return False, ERR_NO_FILE
    return True, None


def validate_image_mime(file_storage):
    try:
        img = Image.open(file_storage.stream)
        img_format = img.format
        file_storage.stream.seek(0)
    except (IOError, OSError, ValueError):
        return False, ERR_INVALID_IMAGE

    if img_format not in ALLOWED_IMAGE_FORMATS:
        return False, ERR_INVALID_IMAGE_FORMAT

    return True, None


def validate_image_size(file_storage, max_bytes=MAX_FILE_SIZE):
    file_storage.stream.seek(0, 2)
    size = file_storage.stream.tell()
    file_storage.stream.seek(0)

    if size > max_bytes:
        return False, ERR_IMAGE_TOO_LARGE.format(max_bytes // (1024 * 1024))

    return True, None


def generate_safe_filename(original_filename):
    extension = os.path.splitext(original_filename)[1].lower()
    if not extension:
        extension = DEFAULT_IMAGE_EXTENSION
    return f"{uuid.uuid4()}{extension}"
