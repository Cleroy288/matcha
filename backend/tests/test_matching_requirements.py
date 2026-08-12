import pytest

from services import browse_service, like_service
from services.errors import ERR_PROFILE_INCOMPLETE


@pytest.mark.parametrize(
    "action",
    [browse_service.browse_suggestions, browse_service.search_profiles],
)
def test_browse_and_search_require_a_complete_profile(monkeypatch, action):
    monkeypatch.setattr(browse_service, "get_profile_by_user_id", lambda _user_id: {"profile_complete": False})

    with pytest.raises(Exception, match=ERR_PROFILE_INCOMPLETE):
        action(7, {})


def test_like_requires_a_complete_profile(monkeypatch):
    monkeypatch.setattr(like_service, "get_profile_by_user_id", lambda _user_id: {"profile_complete": False})

    with pytest.raises(Exception, match=ERR_PROFILE_INCOMPLETE):
        like_service.like_user(7, 8)


def test_browse_returns_all_profile_photos(monkeypatch):
    monkeypatch.setattr(browse_service, "get_profile_by_user_id", lambda _user_id: {"profile_complete": True})
    monkeypatch.setattr(
        browse_service,
        "fetch_candidates",
        lambda _profile, _criteria: [{
            "profile_photo": "main.jpg",
            "photo_paths": ["main.jpg", "second.jpg"],
        }],
    )
    monkeypatch.setattr(browse_service, "build_photo_url", lambda path: f"/uploads/{path}" if path else None)

    result = browse_service.run_candidates_query(7, {})

    assert result[0]["profile_photo_url"] == "/uploads/main.jpg"
    assert result[0]["photo_urls"] == ["/uploads/main.jpg", "/uploads/second.jpg"]
