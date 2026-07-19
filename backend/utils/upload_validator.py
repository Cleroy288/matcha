import os
import uuid

from PIL import Image

from utils.constants import ALLOWED_IMAGE_EXTENSIONS, ALLOWED_IMAGE_FORMATS, MAX_FILE_SIZE
from utils.errors import (
    ERR_IMAGE_TOO_LARGE,
    ERR_INVALID_IMAGE,
    ERR_INVALID_IMAGE_EXTENSION,
    ERR_INVALID_IMAGE_FORMAT,
    ERR_NO_FILE,
)


def validate_image_file(file_storage):
    if not file_storage or file_storage.filename == "":
        return False, ERR_NO_FILE
    return True, None


def validate_image_mime(file_storage):
    try:
        img = Image.open(file_storage.stream)
        img_format = img.format
        file_storage.stream.seek(0)
    except (OSError, ValueError):
        return False, ERR_INVALID_IMAGE

    if img_format not in ALLOWED_IMAGE_FORMATS:
        return False, ERR_INVALID_IMAGE_FORMAT

    return validate_image_extension(file_storage.filename, img_format)


def validate_image_extension(filename, image_format):
    extension = os.path.splitext(filename or "")[1].lower()
    if ALLOWED_IMAGE_EXTENSIONS.get(extension) != image_format:
        return False, ERR_INVALID_IMAGE_EXTENSION
    return True, None


def validate_image_size(file_storage, max_bytes=MAX_FILE_SIZE):
    file_storage.stream.seek(0, 2)
    size = file_storage.stream.tell()
    file_storage.stream.seek(0)

    if size > max_bytes:
        return False, ERR_IMAGE_TOO_LARGE

    return True, None


def generate_safe_filename(original_filename):
    extension = os.path.splitext(original_filename)[1].lower()
    return f"{uuid.uuid4()}{extension}"
