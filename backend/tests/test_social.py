import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

os.environ.setdefault("JWT_EXP_DELTA_SECONDS", "3600")
os.environ.setdefault("FRONTEND_URL", "http://localhost:5173")


@pytest.fixture()
def app():
    from flask import Flask

    from routes.social_routes import social_routes

    test_app = Flask(__name__)
    test_app.config["TESTING"] = True
    test_app.register_blueprint(social_routes)
    return test_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def auth_client(client, mocker):
    """Client avec JWT mocké — simule un user connecté (id=1)."""
    mocker.patch("utils.jwt_required.decode_token", return_value={"user_id": 1})
    client.set_cookie("auth_token", "fake-token")
    return client


# ══════════════════════════════════════════════════════════
# LIKES
# ══════════════════════════════════════════════════════════

class TestLikeRoutes:
    def test_like_success(self, auth_client, mocker):
        mocker.patch("controllers.like_controller.like_user",
                     return_value={"liked": True, "match": False})
        mocker.patch("controllers.like_controller.recalculate_fame")
        res = auth_client.post("/like/2")
        data = json.loads(res.data)

        assert res.status_code == 200
        assert data["liked"] is True
        assert data["match"] is False

    def test_like_match(self, auth_client, mocker):
        mocker.patch("controllers.like_controller.like_user",
                     return_value={"liked": True, "match": True})
        mocker.patch("controllers.like_controller.recalculate_fame")
        res = auth_client.post("/like/2")
        data = json.loads(res.data)

        assert res.status_code == 200
        assert data["match"] is True

    def test_like_yourself(self, auth_client, mocker):
        mocker.patch("controllers.like_controller.like_user",
                     side_effect=Exception("You cannot like yourself"))
        mocker.patch("controllers.like_controller.recalculate_fame")
        res = auth_client.post("/like/1")  # user_id = 1 = soi-même
        data = json.loads(res.data)

        assert res.status_code == 400
        assert "error" in data

    def test_like_already(self, auth_client, mocker):
        mocker.patch("controllers.like_controller.like_user",
                     side_effect=Exception("Already liked"))
        mocker.patch("controllers.like_controller.recalculate_fame")
        res = auth_client.post("/like/2")

        assert res.status_code == 400

    def test_unlike_success(self, auth_client, mocker):
        mocker.patch("controllers.like_controller.unlike_user",
                     return_value={"unliked": True})
        mocker.patch("controllers.like_controller.recalculate_fame")
        res = auth_client.delete("/like/2")
        data = json.loads(res.data)

        assert res.status_code == 200
        assert data["unliked"] is True

    def test_likes_received(self, auth_client, mocker):
        mocker.patch("controllers.like_controller.get_received_likes", return_value=[
            {"id": 2, "username": "userB", "first_name": "B", "last_name": "B", "liked_at": "2026-01-01"}
        ])
        res = auth_client.get("/likes/received")
        data = json.loads(res.data)

        assert res.status_code == 200
        assert len(data["likes"]) == 1
        assert data["likes"][0]["username"] == "userB"

    def test_no_token(self, client):
        """Sans cookie → 401."""
        res = client.post("/like/2")
        assert res.status_code == 401


# ══════════════════════════════════════════════════════════
# PROFILE VIEWS
# ══════════════════════════════════════════════════════════

class TestProfileViewRoutes:
    def test_visit_success(self, auth_client, mocker):
        mocker.patch("controllers.profile_view_controller.view_profile")
        mocker.patch("controllers.profile_view_controller.recalculate_fame")
        res = auth_client.post("/visit/2")
        data = json.loads(res.data)

        assert res.status_code == 200
        assert data["visited"] is True

    def test_views_received(self, auth_client, mocker):
        mocker.patch("controllers.profile_view_controller.get_profile_views", return_value=[
            {"id": 3, "username": "userC", "first_name": "C", "last_name": "C", "viewed_at": "2026-01-01"}
        ])

        res = auth_client.get("/views/received")
        data = json.loads(res.data)

        assert res.status_code == 200
        assert len(data["views"]) == 1


# ══════════════════════════════════════════════════════════
# BLOCKS
# ══════════════════════════════════════════════════════════

class TestBlockRoutes:
    def test_block_success(self, auth_client, mocker):
        mocker.patch("controllers.block_controller.block_user")

        res = auth_client.post("/block/2")
        data = json.loads(res.data)

        assert res.status_code == 200
        assert data["blocked"] is True

    def test_block_yourself(self, auth_client, mocker):
        mocker.patch("controllers.block_controller.block_user",
                     side_effect=Exception("You cannot block yourself"))

        res = auth_client.post("/block/1")

        assert res.status_code == 400

    def test_unblock_success(self, auth_client, mocker):
        mocker.patch("controllers.block_controller.unblock_user")

        res = auth_client.delete("/block/2")
        data = json.loads(res.data)

        assert res.status_code == 200
        assert data["unblocked"] is True


# ══════════════════════════════════════════════════════════
# REPORTS
# ══════════════════════════════════════════════════════════

class TestReportRoutes:
    def test_report_success(self, auth_client, mocker):
        mocker.patch("controllers.report_controller.report_user")
        mocker.patch("controllers.report_controller.recalculate_fame")

        res = auth_client.post("/report/2", json={"reason": "fake account"})
        data = json.loads(res.data)

        assert res.status_code == 200
        assert data["reported"] is True

    def test_report_yourself(self, auth_client, mocker):
        mocker.patch("controllers.report_controller.report_user",
                     side_effect=Exception("You cannot report yourself"))
        mocker.patch("controllers.report_controller.recalculate_fame")
        res = auth_client.post(
            "/report/1",
            json={}  # ← force le cookie
        )
        print(res.data)
        assert res.status_code == 400

    def test_report_no_reason(self, auth_client, mocker):
        """La raison est optionnelle — doit quand même fonctionner."""
        mocker.patch("controllers.report_controller.report_user")
        mocker.patch("controllers.report_controller.recalculate_fame")
        res = auth_client.post("/report/2", json={})

        assert res.status_code == 200


# ══════════════════════════════════════════════════════════
# NOTIFICATIONS
# ══════════════════════════════════════════════════════════

class TestNotificationRoutes:
    def test_get_notifications(self, auth_client, mocker):
        mocker.patch("controllers.notification_controller.get_user_notifications",
                     return_value=[
                         {"id": 1, "type": "like", "is_read": False,
                          "username": "userB", "created_at": "2026-01-01"}
                     ])

        res = auth_client.get("/notifications")
        data = json.loads(res.data)

        assert res.status_code == 200
        assert len(data["notifications"]) == 1
        assert data["notifications"][0]["type"] == "like"

    def test_mark_read(self, auth_client, mocker):
        mocker.patch("controllers.notification_controller.mark_notifications_read")

        res = auth_client.patch("/notifications/read")
        data = json.loads(res.data)

        assert res.status_code == 200
        assert data["ok"] is True

    def test_unread_count(self, auth_client, mocker):
        mocker.patch("controllers.notification_controller.get_unread_count",
                     return_value=3)

        res = auth_client.get("/notifications/unread")
        data = json.loads(res.data)

        assert res.status_code == 200
        assert data["count"] == 3

    def test_unread_count_zero(self, auth_client, mocker):
        mocker.patch("controllers.notification_controller.get_unread_count",
                     return_value=0)

        res = auth_client.get("/notifications/unread")
        data = json.loads(res.data)

        assert res.status_code == 200
        assert data["count"] == 0