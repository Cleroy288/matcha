from io import BytesIO

from PIL import Image
from werkzeug.datastructures import FileStorage

from utils.errors import ERR_INVALID_IMAGE_EXTENSION
from utils.upload_validator import validate_image_mime


def image_file(filename, image_format):
    stream = BytesIO()
    Image.new("RGB", (1, 1)).save(stream, format=image_format)
    stream.seek(0)
    return FileStorage(stream=stream, filename=filename)


def test_image_extension_must_be_allowed_and_match_content():
    assert validate_image_mime(image_file("photo.JPG", "JPEG")) == (True, None)
    assert validate_image_mime(image_file("photo.php", "JPEG")) == (
        False,
        ERR_INVALID_IMAGE_EXTENSION,
    )
    assert validate_image_mime(image_file("photo.jpg", "PNG")) == (
        False,
        ERR_INVALID_IMAGE_EXTENSION,
    )
