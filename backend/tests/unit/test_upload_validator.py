import io
import os
import sys
import uuid
from unittest.mock import MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from utils.errors import (
    ERR_IMAGE_TOO_LARGE,
    ERR_INVALID_IMAGE,
    ERR_INVALID_IMAGE_FORMAT,
    ERR_NO_FILE,
)
from utils.upload_validator import (
    generate_safe_filename,
    validate_image_file,
    validate_image_mime,
    validate_image_size,
)


def make_file_storage(filename="photo.jpg", content=b"fake-image-data"):
    mock = MagicMock()
    mock.filename = filename
    mock.stream = io.BytesIO(content)
    return mock


class TestValidateImageFile:
    def test_valid_file(self):
        file = make_file_storage()
        valid, error = validate_image_file(file)
        assert valid is True
        assert error is None

    def test_none_file(self):
        valid, error = validate_image_file(None)
        assert valid is False
        assert error == ERR_NO_FILE

    def test_empty_filename(self):
        file = make_file_storage(filename="")
        valid, error = validate_image_file(file)
        assert valid is False
        assert error == ERR_NO_FILE


class TestValidateImageMime:
    def test_valid_jpeg(self, mocker):
        mock_img = MagicMock()
        mock_img.format = "JPEG"
        mocker.patch("utils.upload_validator.Image.open", return_value=mock_img)

        file = make_file_storage()
        valid, error = validate_image_mime(file)
        assert valid is True
        assert error is None

    def test_corrupted_file(self, mocker):
        mocker.patch("utils.upload_validator.Image.open", side_effect=OSError("corrupt"))

        file = make_file_storage()
        valid, error = validate_image_mime(file)
        assert valid is False
        assert error == ERR_INVALID_IMAGE

    def test_unsupported_format(self, mocker):
        mock_img = MagicMock()
        mock_img.format = "BMP"
        mocker.patch("utils.upload_validator.Image.open", return_value=mock_img)

        file = make_file_storage()
        valid, error = validate_image_mime(file)
        assert valid is False
        assert error == ERR_INVALID_IMAGE_FORMAT


class TestValidateImageSize:
    def test_valid_size(self):
        content = b"x" * (1024 * 1024)
        file = make_file_storage(content=content)
        valid, error = validate_image_size(file)
        assert valid is True
        assert error is None

    def test_file_too_large(self):
        content = b"x" * (6 * 1024 * 1024)
        file = make_file_storage(content=content)
        valid, error = validate_image_size(file)
        assert valid is False
        assert error == ERR_IMAGE_TOO_LARGE


class TestGenerateSafeFilename:
    def test_preserves_extension(self):
        result = generate_safe_filename("photo.jpg")
        assert result.endswith(".jpg")
        name_part = result.replace(".jpg", "")
        uuid.UUID(name_part)

    def test_no_extension_defaults_to_jpg(self):
        result = generate_safe_filename("noextension")
        assert result.endswith(".jpg")
