from flask import Blueprint
from controllers.like_controller import like, unlike, likes_received
from controllers.profile_view_controller import visit, views_received
from controllers.block_controller import block, unblock
from controllers.report_controller import report
from controllers.notification_controller import get_notifications, read_notifications, unread_count

social_routes = Blueprint("social", __name__)

# Likes
social_routes.route("/like/<int:user_id>",    methods=["POST"])(like)
social_routes.route("/like/<int:user_id>",    methods=["DELETE"])(unlike)
social_routes.route("/likes/received",        methods=["GET"])(likes_received)

# Profile views
social_routes.route("/visit/<int:user_id>",   methods=["POST"])(visit)
social_routes.route("/views/received",        methods=["GET"])(views_received)

# Blocks
social_routes.route("/block/<int:user_id>",   methods=["POST"])(block)
social_routes.route("/block/<int:user_id>",   methods=["DELETE"])(unblock)

# Reports
social_routes.route("/report/<int:user_id>",  methods=["POST"])(report)

# Notifications
social_routes.route("/notifications",         methods=["GET"])(get_notifications)
social_routes.route("/notifications/read",    methods=["PATCH"])(read_notifications)
social_routes.route("/notifications/unread",  methods=["GET"])(unread_count)