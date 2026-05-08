from flask import Blueprint
from controllers.profile_controller import (
    get_profile, get_public_profile, update_profile, update_location,
    add_tag, remove_tag, search_tags,
    upload_photo_handler, delete_photo, set_profile_photo
)

profile_routes = Blueprint("profile", __name__)

profile_routes.route("/profile", methods=["GET"])(get_profile)
profile_routes.route("/profile/<int:user_id>", methods=["GET"])(get_public_profile)
profile_routes.route("/profile", methods=["PUT"])(update_profile)
profile_routes.route("/profile/location", methods=["PUT"])(update_location)
profile_routes.route("/profile/tags", methods=["POST"])(add_tag)
profile_routes.route("/profile/tags", methods=["DELETE"])(remove_tag)
profile_routes.route("/tags/search", methods=["GET"])(search_tags)
profile_routes.route("/profile/photos", methods=["POST"])(upload_photo_handler)
profile_routes.route("/profile/photos/<int:photo_id>", methods=["DELETE"])(delete_photo)
profile_routes.route("/profile/photos/<int:photo_id>/profile", methods=["PUT"])(set_profile_photo)
