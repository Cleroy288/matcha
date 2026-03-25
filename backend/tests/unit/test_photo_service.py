import io
import os
import sys
from unittest.mock import MagicMock

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest-32bytes!")
os.environ.setdefault("FRONTEND_URL", "http://localhost:5173")

from services.errors import ERR_MAX_PHOTOS, ERR_NOT_AUTHORIZED, ERR_PHOTO_NOT_FOUND
from services.photo_service import (
    delete_user_photo,
    get_user_photos,
    set_user_profile_photo,
    upload_photo,
)

FAKE_PHOTO = {"id": 1, "user_id": 1, "file_path": "abc.jpg", "is_profile": True, "sort_order": 0}


def make_valid_file_storage():
    mock = MagicMock()
    mock.filename = "photo.jpg"
    mock.stream = io.BytesIO(b"x" * 1024)
    mock.save = MagicMock()
    return mock


class TestUploadPhoto:
    def test_success(self, mocker):
        mocker.patch("services.photo_service.count_user_photos", return_value=0)
        mocker.patch("services.photo_service.validate_image_file", return_value=(True, None))
        mocker.patch("services.photo_service.validate_image_mime", return_value=(True, None))
        mocker.patch("services.photo_service.validate_image_size", return_value=(True, None))
        mocker.patch("services.photo_service.generate_safe_filename", return_value="safe-uuid.jpg")
        mocker.patch("services.photo_service.os.makedirs")
        mocker.patch("services.photo_service.create_photo", return_value=FAKE_PHOTO)
        mocker.patch("services.photo_service.check_profile_completeness")

        file = make_valid_file_storage()
        result = upload_photo(1, file)
        assert result == FAKE_PHOTO

    def test_first_photo_is_profile(self, mocker):
        mocker.patch("services.photo_service.count_user_photos", return_value=0)
        mocker.patch("services.photo_service.validate_image_file", return_value=(True, None))
        mocker.patch("services.photo_service.validate_image_mime", return_value=(True, None))
        mocker.patch("services.photo_service.validate_image_size", return_value=(True, None))
        mocker.patch("services.photo_service.generate_safe_filename", return_value="safe-uuid.jpg")
        mocker.patch("services.photo_service.os.makedirs")
        mock_create = mocker.patch("services.photo_service.create_photo", return_value=FAKE_PHOTO)
        mocker.patch("services.photo_service.check_profile_completeness")

        file = make_valid_file_storage()
        upload_photo(1, file)
        mock_create.assert_called_once_with(1, "safe-uuid.jpg", True, 0)

    def test_max_photos_reached(self, mocker):
        mocker.patch("services.photo_service.count_user_photos", return_value=5)

        with pytest.raises(Exception, match=ERR_MAX_PHOTOS):
            upload_photo(1, make_valid_file_storage())

    def test_invalid_file(self, mocker):
        mocker.patch("services.photo_service.count_user_photos", return_value=0)
        mocker.patch("services.photo_service.validate_image_file", return_value=(False, "No file provided"))

        with pytest.raises(Exception, match="No file provided"):
            upload_photo(1, make_valid_file_storage())

    def test_db_error_rolls_back_file(self, mocker):
        mocker.patch("services.photo_service.count_user_photos", return_value=0)
        mocker.patch("services.photo_service.validate_image_file", return_value=(True, None))
        mocker.patch("services.photo_service.validate_image_mime", return_value=(True, None))
        mocker.patch("services.photo_service.validate_image_size", return_value=(True, None))
        mocker.patch("services.photo_service.generate_safe_filename", return_value="safe-uuid.jpg")
        mocker.patch("services.photo_service.os.makedirs")
        mocker.patch("services.photo_service.create_photo", side_effect=Exception("DB error"))
        mocker.patch("services.photo_service.os.path.exists", return_value=True)
        mock_remove = mocker.patch("services.photo_service.os.remove")

        file = make_valid_file_storage()
        with pytest.raises(Exception, match="DB error"):
            upload_photo(1, file)
        mock_remove.assert_called_once()


class TestDeleteUserPhoto:
    def test_success(self, mocker):
        mocker.patch("services.photo_service.get_photo_by_id", return_value=dict(FAKE_PHOTO, is_profile=False))
        mocker.patch("services.photo_service.delete_photo", return_value={"file_path": "abc.jpg"})
        mocker.patch("services.photo_service.os.path.exists", return_value=True)
        mocker.patch("services.photo_service.os.remove")
        mocker.patch("services.photo_service.check_profile_completeness")

        delete_user_photo(1, 1)

    def test_photo_not_found(self, mocker):
        mocker.patch("services.photo_service.get_photo_by_id", return_value=None)

        with pytest.raises(Exception, match=ERR_PHOTO_NOT_FOUND):
            delete_user_photo(1, 999)

    def test_not_authorized(self, mocker):
        mocker.patch("services.photo_service.get_photo_by_id", return_value=dict(FAKE_PHOTO, user_id=2))

        with pytest.raises(Exception, match=ERR_NOT_AUTHORIZED):
            delete_user_photo(1, 1)

    def test_profile_photo_reassigned(self, mocker):
        mocker.patch("services.photo_service.get_photo_by_id", return_value=dict(FAKE_PHOTO, is_profile=True))
        mocker.patch("services.photo_service.delete_photo", return_value={"file_path": "abc.jpg"})
        mocker.patch("services.photo_service.os.path.exists", return_value=False)
        remaining = [{"id": 2, "user_id": 1, "file_path": "other.jpg", "is_profile": False}]
        mocker.patch("services.photo_service.get_photos_by_user", return_value=remaining)
        mock_set = mocker.patch("services.photo_service.set_profile_photo")
        mocker.patch("services.photo_service.check_profile_completeness")

        delete_user_photo(1, 1)
        mock_set.assert_called_once_with(1, 2)


class TestSetUserProfilePhoto:
    def test_success(self, mocker):
        mocker.patch("services.photo_service.get_photo_by_id", return_value=FAKE_PHOTO)
        mocker.patch("services.photo_service.set_profile_photo")

        set_user_profile_photo(1, 1)

    def test_photo_not_found(self, mocker):
        mocker.patch("services.photo_service.get_photo_by_id", return_value=None)

        with pytest.raises(Exception, match=ERR_PHOTO_NOT_FOUND):
            set_user_profile_photo(1, 999)

    def test_not_authorized(self, mocker):
        mocker.patch("services.photo_service.get_photo_by_id", return_value=dict(FAKE_PHOTO, user_id=2))

        with pytest.raises(Exception, match=ERR_NOT_AUTHORIZED):
            set_user_profile_photo(1, 1)


class TestGetUserPhotos:
    def test_returns_photos(self, mocker):
        photos = [FAKE_PHOTO]
        mocker.patch("services.photo_service.get_photos_by_user", return_value=photos)

        result = get_user_photos(1)
        assert result == photos
