import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest-32bytes!")
os.environ.setdefault("FRONTEND_URL", "http://localhost:5173")

from services.errors import (
    ERR_MAX_TAGS,
    ERR_SEARCH_QUERY_REQUIRED,
    ERR_TAG_CREATION_FAILED,
    ERR_TAG_NOT_FOUND,
)
from services.tag_service import (
    add_tag_to_profile,
    get_user_profile_tags,
    remove_tag_from_profile,
    search_available_tags,
)

FAKE_TAGS = [{"id": 1, "name": "#python"}, {"id": 2, "name": "#flask"}]


class TestAddTagToProfile:
    def test_success(self, mocker):
        mocker.patch("services.tag_service.count_user_tags", return_value=0)
        mocker.patch("services.tag_service.create_tag", return_value={"id": 3, "name": "#react"})
        mocker.patch("services.tag_service.add_tag_to_user")
        mocker.patch("services.tag_service.check_profile_completeness")
        mocker.patch("services.tag_service.get_user_tags", return_value=FAKE_TAGS + [{"id": 3, "name": "#react"}])

        result = add_tag_to_profile(1, "#react")
        assert len(result) == 3

    def test_invalid_tag_format(self, mocker):
        with pytest.raises(Exception, match="Tag must start with"):
            add_tag_to_profile(1, "nohash")

    def test_max_tags_reached(self, mocker):
        mocker.patch("services.tag_service.count_user_tags", return_value=10)

        with pytest.raises(Exception, match=ERR_MAX_TAGS):
            add_tag_to_profile(1, "#newtag")

    def test_tag_creation_failed(self, mocker):
        mocker.patch("services.tag_service.count_user_tags", return_value=0)
        mocker.patch("services.tag_service.create_tag", return_value=None)

        with pytest.raises(Exception, match=ERR_TAG_CREATION_FAILED):
            add_tag_to_profile(1, "#newtag")


class TestRemoveTagFromProfile:
    def test_success(self, mocker):
        mocker.patch("services.tag_service.get_user_tags", side_effect=[FAKE_TAGS, [FAKE_TAGS[1]]])
        mocker.patch("services.tag_service.remove_tag_from_user")
        mocker.patch("services.tag_service.check_profile_completeness")

        result = remove_tag_from_profile(1, "#python")
        assert len(result) == 1

    def test_tag_not_found(self, mocker):
        mocker.patch("services.tag_service.get_user_tags", return_value=FAKE_TAGS)

        with pytest.raises(Exception, match=ERR_TAG_NOT_FOUND):
            remove_tag_from_profile(1, "#nonexistent")


class TestGetUserProfileTags:
    def test_returns_tags(self, mocker):
        mocker.patch("services.tag_service.get_user_tags", return_value=FAKE_TAGS)

        result = get_user_profile_tags(1)
        assert result == FAKE_TAGS


class TestSearchAvailableTags:
    def test_success(self, mocker):
        mocker.patch("services.tag_service.search_tags", return_value=FAKE_TAGS)

        result = search_available_tags("py")
        assert len(result) == 2

    def test_empty_query(self):
        with pytest.raises(Exception, match=ERR_SEARCH_QUERY_REQUIRED):
            search_available_tags("")
