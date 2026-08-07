from flask import Blueprint

from controllers.profile_controller import (
    add_tag,
    delete_account,
    delete_photo,
    get_profile,
    get_public_profile,
    remove_tag,
    search_tags,
    set_profile_photo,
    update_location,
    update_profile,
    upload_photo_handler,
)

profile_routes = Blueprint("profile", __name__)

profile_routes.route("/profile", methods=["GET"])(get_profile)
profile_routes.route("/profile/<int:user_id>", methods=["GET"])(get_public_profile)
profile_routes.route("/profile", methods=["PUT"])(update_profile)
profile_routes.route("/profile", methods=["DELETE"])(delete_account)
profile_routes.route("/profile/location", methods=["PUT"])(update_location)
profile_routes.route("/profile/tags", methods=["POST"])(add_tag)
profile_routes.route("/profile/tags", methods=["DELETE"])(remove_tag)
profile_routes.route("/tags/search", methods=["GET"])(search_tags)
profile_routes.route("/profile/photos", methods=["POST"])(upload_photo_handler)
profile_routes.route("/profile/photos/<int:photo_id>", methods=["DELETE"])(delete_photo)
profile_routes.route("/profile/photos/<int:photo_id>/profile", methods=["PUT"])(set_profile_photo)
