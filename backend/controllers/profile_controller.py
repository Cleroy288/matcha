from flask import jsonify, request

from controllers.constants import HTTP_BAD_REQUEST, HTTP_CREATED, HTTP_NOT_FOUND, HTTP_OK
from controllers.errors import MSG_LOCATION_UPDATED, MSG_PHOTO_DELETED, MSG_PROFILE_PHOTO_UPDATED
from services.photo_service import delete_user_photo, set_user_profile_photo, upload_photo
from services.profile_service import get_full_profile, update_user_location, update_user_profile
from services.tag_service import add_tag_to_profile, remove_tag_from_profile, search_available_tags
from utils.jwt_required import jwt_required


@jwt_required
def get_profile(payload):
    user_id = payload["user_id"]
    try:
        profile = get_full_profile(user_id)
        return jsonify(profile), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST

@jwt_required
def get_public_profile(payload, user_id):
    from services.profile_service import get_public_profile_data
    data = get_public_profile_data(payload["user_id"], user_id)
    if not data:
        return jsonify({"error": "Not found"}), HTTP_NOT_FOUND
    return jsonify(data), HTTP_OK

@jwt_required
def update_profile(payload):
    user_id = payload["user_id"]
    data = request.json
    try:
        profile = update_user_profile(user_id, data)
        return jsonify(profile), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST


@jwt_required
def update_location(payload):
    user_id = payload["user_id"]
    data = request.json
    try:
        update_user_location(
            user_id,
            data.get("latitude"),
            data.get("longitude"),
            data.get("city", ""),
            data.get("gps_consent", False)
        )
        return jsonify({"message": MSG_LOCATION_UPDATED}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST


@jwt_required
def add_tag(payload):
    user_id = payload["user_id"]
    data = request.json
    try:
        tags = add_tag_to_profile(user_id, data.get("name", ""))
        return jsonify({"tags": tags}), HTTP_CREATED
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST


@jwt_required
def remove_tag(payload):
    user_id = payload["user_id"]
    data = request.json
    try:
        tags = remove_tag_from_profile(user_id, data.get("name", ""))
        return jsonify({"tags": tags}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST


@jwt_required
def search_tags(_payload):
    query = request.args.get("q", "")
    try:
        tags = search_available_tags(query)
        return jsonify({"tags": tags}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST


@jwt_required
def upload_photo_handler(payload):
    user_id = payload["user_id"]
    file = request.files.get("photo")
    try:
        photo = upload_photo(user_id, file)
        return jsonify(photo), HTTP_CREATED
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST


@jwt_required
def delete_photo(payload, photo_id):
    user_id = payload["user_id"]
    try:
        delete_user_photo(user_id, photo_id)
        return jsonify({"message": MSG_PHOTO_DELETED}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST


@jwt_required
def set_profile_photo(payload, photo_id):
    user_id = payload["user_id"]
    try:
        set_user_profile_photo(user_id, photo_id)
        return jsonify({"message": MSG_PROFILE_PHOTO_UPDATED}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST
