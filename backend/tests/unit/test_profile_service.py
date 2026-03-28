import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest-32bytes!")
os.environ.setdefault("FRONTEND_URL", "http://localhost:5173")

from services.errors import ERR_NO_FIELDS_TO_UPDATE
from services.profile_service import (
    check_profile_completeness,
    get_full_profile,
    get_or_create_profile,
    update_user_location,
    update_user_profile,
)

FAKE_PROFILE = {
    "id": 1,
    "user_id": 1,
    "gender": "male",
    "sexual_preference": "bisexual",
    "biography": "Hello",
    "birth_date": "2000-01-01",
    "fame_rating": 0,
    "latitude": None,
    "longitude": None,
    "city": None,
    "gps_consent": False,
    "profile_complete": False,
}

FAKE_USER = {
    "id": 1,
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User",
    "email": "test@test.com",
}


class TestGetOrCreateProfile:
    def test_profile_exists(self, mocker):
        mocker.patch("services.profile_service.get_profile_by_user_id", return_value=FAKE_PROFILE)

        result = get_or_create_profile(1)
        assert result == FAKE_PROFILE

    def test_profile_not_exists_creates(self, mocker):
        mocker.patch("services.profile_service.get_profile_by_user_id", return_value=None)
        mocker.patch("services.profile_service.create_profile", return_value=FAKE_PROFILE)

        result = get_or_create_profile(1)
        assert result == FAKE_PROFILE


class TestGetFullProfile:
    def test_returns_complete_profile(self, mocker):
        mocker.patch("services.profile_service.get_or_create_profile", return_value=dict(FAKE_PROFILE))
        mocker.patch("services.profile_service.get_user_by_id", return_value=FAKE_USER)
        mocker.patch("services.profile_service.get_user_tags", return_value=[{"id": 1, "name": "#python"}])
        mocker.patch("services.profile_service.get_photos_by_user", return_value=[])

        result = get_full_profile(1)
        assert result["username"] == "testuser"
        assert result["tags"] == [{"id": 1, "name": "#python"}]
        assert result["photos"] == []


class TestUpdateUserProfile:
    def test_valid_update(self, mocker):
        mocker.patch("services.profile_service.get_or_create_profile", return_value=FAKE_PROFILE)
        mocker.patch("services.profile_service.update_profile")
        mocker.patch("services.profile_service.check_profile_completeness")
        updated = dict(FAKE_PROFILE, gender="female")
        updated["username"] = "testuser"
        updated["first_name"] = "Test"
        updated["last_name"] = "User"
        updated["email"] = "test@test.com"
        updated["tags"] = []
        updated["photos"] = []
        mocker.patch("services.profile_service.get_full_profile", return_value=updated)

        result = update_user_profile(1, {"gender": "female"})
        assert result["gender"] == "female"

    def test_no_fields(self, mocker):
        mocker.patch("services.profile_service.get_or_create_profile", return_value=FAKE_PROFILE)

        with pytest.raises(Exception, match=ERR_NO_FIELDS_TO_UPDATE):
            update_user_profile(1, {})

    def test_invalid_gender(self, mocker):
        mocker.patch("services.profile_service.get_or_create_profile", return_value=FAKE_PROFILE)

        with pytest.raises(Exception, match="Gender must be"):
            update_user_profile(1, {"gender": "alien"})


class TestUpdateUserLocation:
    def test_valid_location(self, mocker):
        mocker.patch("services.profile_service.get_or_create_profile", return_value=FAKE_PROFILE)
        mocker.patch("services.profile_service.update_location")

        update_user_location(1, 48.8, 2.3, "Paris", True)

    def test_invalid_coordinates(self, mocker):
        mocker.patch("services.profile_service.get_or_create_profile", return_value=FAKE_PROFILE)

        with pytest.raises(Exception, match="must be numbers"):
            update_user_location(1, "abc", "def", "Paris", True)

    def test_invalid_city(self, mocker):
        mocker.patch("services.profile_service.get_or_create_profile", return_value=FAKE_PROFILE)

        with pytest.raises(Exception, match="City must be"):
            update_user_location(1, 48.8, 2.3, "x" * 101, True)


class TestCheckProfileCompleteness:
    def test_complete_profile(self, mocker):
        complete = dict(FAKE_PROFILE, gender="male", biography="Bio", birth_date="2000-01-01")
        mocker.patch("services.profile_service.get_profile_by_user_id", return_value=complete)
        mocker.patch("services.profile_service.count_user_tags", return_value=1)
        mocker.patch("services.profile_service.count_user_photos", return_value=1)
        mock_set = mocker.patch("services.profile_service.set_profile_complete")

        check_profile_completeness(1)
        mock_set.assert_called_once_with(1, True)

    def test_incomplete_profile(self, mocker):
        incomplete = dict(FAKE_PROFILE, gender=None, biography=None, birth_date=None)
        mocker.patch("services.profile_service.get_profile_by_user_id", return_value=incomplete)
        mocker.patch("services.profile_service.count_user_tags", return_value=0)
        mocker.patch("services.profile_service.count_user_photos", return_value=0)
        mock_set = mocker.patch("services.profile_service.set_profile_complete")

        check_profile_completeness(1)
        mock_set.assert_called_once_with(1, False)

    def test_no_profile(self, mocker):
        mocker.patch("services.profile_service.get_profile_by_user_id", return_value=None)

        check_profile_completeness(1)
