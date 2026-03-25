import io
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest-32bytes!")
os.environ.setdefault("JWT_EXP_DELTA_SECONDS", "3600")
os.environ.setdefault("FRONTEND_URL", "http://localhost:5173")

from controllers.errors import MSG_LOCATION_UPDATED, MSG_PHOTO_DELETED, MSG_PROFILE_PHOTO_UPDATED

FAKE_PROFILE = {
    "id": 1,
    "user_id": 1,
    "gender": "male",
    "sexual_preference": "bisexual",
    "biography": "Hello",
    "birth_date": "2000-01-01",
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User",
    "email": "test@test.com",
    "tags": [],
    "photos": [],
}

FAKE_TAGS = [{"id": 1, "name": "#python"}, {"id": 2, "name": "#flask"}]

FAKE_PHOTO = {"id": 1, "user_id": 1, "file_path": "abc.jpg", "is_profile": True, "sort_order": 0}

AUTH_HEADERS = {"Authorization": "Bearer valid-token", "Content-Type": "application/json"}


@pytest.fixture()
def app():
    from flask import Flask

    from routes.profile_routes import profile_routes

    test_app = Flask(__name__)
    test_app.config["TESTING"] = True
    test_app.config["SECRET_KEY"] = "test-secret-key-for-pytest-32bytes!"
    test_app.register_blueprint(profile_routes)
    return test_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def mock_jwt(mocker):
    mocker.patch("utils.jwt_required.decode_token", return_value={"user_id": 1})


class TestGetProfileRoute:
    def test_success(self, client, mocker):
        mocker.patch("controllers.profile_controller.get_full_profile", return_value=FAKE_PROFILE)

        response = client.get("/profile", headers=AUTH_HEADERS)
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data["username"] == "testuser"

    def test_no_token(self, client, mocker):
        mocker.patch("utils.jwt_required.decode_token", side_effect=Exception("Token missing"))

        response = client.get("/profile")
        assert response.status_code == 401


class TestUpdateProfileRoute:
    def test_success(self, client, mocker):
        updated = dict(FAKE_PROFILE, gender="female")
        mocker.patch("controllers.profile_controller.update_user_profile", return_value=updated)

        response = client.put("/profile", headers=AUTH_HEADERS, json={"gender": "female"})
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data["gender"] == "female"

    def test_error(self, client, mocker):
        mocker.patch(
            "controllers.profile_controller.update_user_profile",
            side_effect=Exception("No valid fields to update"),
        )

        response = client.put("/profile", headers=AUTH_HEADERS, json={})
        assert response.status_code == 400


class TestUpdateLocationRoute:
    def test_success(self, client, mocker):
        mocker.patch("controllers.profile_controller.update_user_location")

        response = client.put(
            "/profile/location",
            headers=AUTH_HEADERS,
            json={"latitude": 48.8, "longitude": 2.3, "city": "Paris", "gps_consent": True},
        )
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data["message"] == MSG_LOCATION_UPDATED

    def test_error(self, client, mocker):
        mocker.patch(
            "controllers.profile_controller.update_user_location",
            side_effect=Exception("Invalid coordinates"),
        )

        response = client.put(
            "/profile/location",
            headers=AUTH_HEADERS,
            json={"latitude": "abc", "longitude": "def"},
        )
        assert response.status_code == 400


class TestAddTagRoute:
    def test_success(self, client, mocker):
        mocker.patch("controllers.profile_controller.add_tag_to_profile", return_value=FAKE_TAGS)

        response = client.post("/profile/tags", headers=AUTH_HEADERS, json={"name": "#python"})
        data = json.loads(response.data)
        assert response.status_code == 201
        assert len(data["tags"]) == 2

    def test_error(self, client, mocker):
        mocker.patch(
            "controllers.profile_controller.add_tag_to_profile",
            side_effect=Exception("Tag must start with #"),
        )

        response = client.post("/profile/tags", headers=AUTH_HEADERS, json={"name": "nohash"})
        assert response.status_code == 400


class TestRemoveTagRoute:
    def test_success(self, client, mocker):
        mocker.patch("controllers.profile_controller.remove_tag_from_profile", return_value=[FAKE_TAGS[1]])

        response = client.delete("/profile/tags", headers=AUTH_HEADERS, json={"name": "#python"})
        data = json.loads(response.data)
        assert response.status_code == 200
        assert len(data["tags"]) == 1

    def test_error(self, client, mocker):
        mocker.patch(
            "controllers.profile_controller.remove_tag_from_profile",
            side_effect=Exception("Tag not found on your profile"),
        )

        response = client.delete("/profile/tags", headers=AUTH_HEADERS, json={"name": "#nonexistent"})
        assert response.status_code == 400


class TestSearchTagsRoute:
    def test_success(self, client, mocker):
        mocker.patch("controllers.profile_controller.search_available_tags", return_value=FAKE_TAGS)

        response = client.get("/tags/search?q=py", headers=AUTH_HEADERS)
        data = json.loads(response.data)
        assert response.status_code == 200
        assert len(data["tags"]) == 2

    def test_error(self, client, mocker):
        mocker.patch(
            "controllers.profile_controller.search_available_tags",
            side_effect=Exception("Search query is required"),
        )

        response = client.get("/tags/search?q=", headers=AUTH_HEADERS)
        assert response.status_code == 400


class TestUploadPhotoRoute:
    def test_success(self, client, mocker):
        mocker.patch("controllers.profile_controller.upload_photo", return_value=FAKE_PHOTO)

        data = {"photo": (io.BytesIO(b"fake-image"), "photo.jpg")}
        response = client.post(
            "/profile/photos",
            headers={"Authorization": "Bearer valid-token"},
            data=data,
            content_type="multipart/form-data",
        )
        resp_data = json.loads(response.data)
        assert response.status_code == 201
        assert resp_data["id"] == 1

    def test_error(self, client, mocker):
        mocker.patch(
            "controllers.profile_controller.upload_photo",
            side_effect=Exception("No file provided"),
        )

        response = client.post(
            "/profile/photos",
            headers={"Authorization": "Bearer valid-token"},
            content_type="multipart/form-data",
        )
        assert response.status_code == 400


class TestDeletePhotoRoute:
    def test_success(self, client, mocker):
        mocker.patch("controllers.profile_controller.delete_user_photo")

        response = client.delete("/profile/photos/1", headers=AUTH_HEADERS)
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data["message"] == MSG_PHOTO_DELETED

    def test_error(self, client, mocker):
        mocker.patch(
            "controllers.profile_controller.delete_user_photo",
            side_effect=Exception("Photo not found"),
        )

        response = client.delete("/profile/photos/999", headers=AUTH_HEADERS)
        assert response.status_code == 400


class TestSetProfilePhotoRoute:
    def test_success(self, client, mocker):
        mocker.patch("controllers.profile_controller.set_user_profile_photo")

        response = client.put("/profile/photos/1/profile", headers=AUTH_HEADERS)
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data["message"] == MSG_PROFILE_PHOTO_UPDATED

    def test_error(self, client, mocker):
        mocker.patch(
            "controllers.profile_controller.set_user_profile_photo",
            side_effect=Exception("Photo not found"),
        )

        response = client.put("/profile/photos/999/profile", headers=AUTH_HEADERS)
        assert response.status_code == 400
