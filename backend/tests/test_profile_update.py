from models import browse_model
from services import profile_service


def test_update_profile_saves_user_and_profile_fields(monkeypatch):
    user_updates = []
    profile_updates = []

    monkeypatch.setattr(profile_service, "get_or_create_profile", lambda _user_id: {})
    monkeypatch.setattr(profile_service, "get_user_by_email", lambda _email: None)
    monkeypatch.setattr(profile_service, "update_user", lambda user_id, fields: user_updates.append((user_id, fields)))
    monkeypatch.setattr(
        profile_service,
        "update_profile",
        lambda user_id, fields: profile_updates.append((user_id, fields)),
    )
    monkeypatch.setattr(profile_service, "check_profile_completeness", lambda _user_id: None)
    monkeypatch.setattr(profile_service, "get_full_profile", lambda _user_id: {"saved": True})

    result = profile_service.update_user_profile(7, {
        "first_name": " Ada ",
        "last_name": " Lovelace ",
        "email": "ada@example.com",
        "gender": "female",
    })

    assert result == {"saved": True}
    assert user_updates == [(7, {
        "first_name": "Ada",
        "last_name": "Lovelace",
        "email": "ada@example.com",
    })]
    assert profile_updates == [(7, {"gender": "female"})]


def test_manual_location_accepts_city_without_coordinates(monkeypatch):
    profile = {
        "gender": "female",
        "sexual_preference": "male",
        "biography": "Hello",
        "birth_date": "2000-01-01",
        "gps_consent": False,
        "latitude": None,
        "longitude": None,
        "city": None,
    }
    location_updates = []
    completion_updates = []

    monkeypatch.setattr(profile_service, "get_or_create_profile", lambda _user_id: profile)
    monkeypatch.setattr(profile_service, "get_profile_by_user_id", lambda _user_id: profile)
    monkeypatch.setattr(profile_service, "count_user_tags", lambda _user_id: 5)
    monkeypatch.setattr(profile_service, "get_photos_by_user", lambda _user_id: [{"is_profile": True}])
    monkeypatch.setattr(
        profile_service,
        "update_location",
        lambda user_id, lat, lng, city, consent: (
            location_updates.append((user_id, lat, lng, city, consent)),
            profile.update(latitude=lat, longitude=lng, city=city, gps_consent=consent),
        ),
    )
    monkeypatch.setattr(
        profile_service,
        "set_profile_complete",
        lambda user_id, complete: completion_updates.append((user_id, complete)),
    )

    profile_service.update_user_location(7, None, None, " Bruxelles ", False)

    assert location_updates == [(7, None, None, "Bruxelles", False)]
    assert completion_updates == [(7, True)]


def test_profile_complete_requires_preference_five_tags_and_primary_photo(monkeypatch):
    profile = {
        "gender": "female",
        "sexual_preference": None,
        "biography": "Hello",
        "birth_date": "2000-01-01",
        "gps_consent": False,
        "latitude": None,
        "longitude": None,
        "city": "Bruxelles",
    }
    tag_count = {"value": 5}
    photos = [{"is_profile": True}]
    completion_updates = []

    monkeypatch.setattr(profile_service, "get_profile_by_user_id", lambda _user_id: profile)
    monkeypatch.setattr(profile_service, "count_user_tags", lambda _user_id: tag_count["value"])
    monkeypatch.setattr(profile_service, "get_photos_by_user", lambda _user_id: photos)
    monkeypatch.setattr(
        profile_service,
        "set_profile_complete",
        lambda _user_id, complete: completion_updates.append(complete),
    )

    profile_service.check_profile_completeness(7)
    profile["sexual_preference"] = "male"
    tag_count["value"] = 4
    profile_service.check_profile_completeness(7)
    tag_count["value"] = 5
    photos[0]["is_profile"] = False
    profile_service.check_profile_completeness(7)
    photos[0]["is_profile"] = True
    profile_service.check_profile_completeness(7)

    assert completion_updates == [False, False, False, True]


def test_suggestion_score_uses_manual_city():
    params = browse_model.build_base_params(
        {"id": 7, "gender": "female", "city": "Bruxelles"},
        {"limit": 50, "offset": 0},
    )

    assert params["me_city"] == "Bruxelles"
    assert "same_city" in browse_model.SCORE_SQL


def test_candidates_require_complete_profile_and_location(monkeypatch):
    queries = []
    monkeypatch.setattr(
        browse_model,
        "run_query",
        lambda query, _params: queries.append(query) or [],
    )

    browse_model.fetch_candidates(
        {"id": 7, "gender": "female", "city": "Bruxelles"},
        {"limit": 50, "offset": 0},
    )

    assert "p.profile_complete = TRUE" in queries[0]
    assert "p.gps_consent = TRUE" in queries[0]
    assert "NULLIF(BTRIM(p.city), '') IS NOT NULL" in queries[0]
