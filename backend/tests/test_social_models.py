from unittest.mock import MagicMock

from models import like_model, profile_view_model, user_model


def fake_database(rows):
    connection = MagicMock()
    cursor = connection.cursor.return_value
    cursor.fetchall.return_value = rows
    return connection, cursor


def test_get_likes_received_uses_valid_query(monkeypatch):
    row = {"id": 2, "username": "alice", "liked_at": "2026-01-01"}
    connection, cursor = fake_database([row])
    monkeypatch.setattr(like_model, "get_connection", lambda: connection)

    assert like_model.get_likes_received(7) == [row]
    query, params = cursor.execute.call_args.args
    assert "SELECT u.id, u.username" in query
    assert params == (7,)


def test_get_views_received_uses_valid_query(monkeypatch):
    row = {"id": 3, "username": "bob", "viewed_at": "2026-01-02"}
    connection, cursor = fake_database([row])
    monkeypatch.setattr(profile_view_model, "get_connection", lambda: connection)

    assert profile_view_model.get_views_received(7) == [row]
    query, params = cursor.execute.call_args.args
    assert "u.id = pv.viewer_id" in query
    assert params == (7,)


def test_login_user_query_includes_profile_completion(monkeypatch):
    connection, cursor = fake_database([])
    cursor.fetchone.return_value = (
        7, "ada@example.com", "ada", "hash", "Ada", "Lovelace", True, False,
    )
    monkeypatch.setattr(user_model, "get_connection", lambda: connection)

    user = user_model.get_user_by_username("ada")

    query, params = cursor.execute.call_args.args
    assert "LEFT JOIN profiles" in query
    assert params == ("ada",)
    assert user["profile_complete"] is False
