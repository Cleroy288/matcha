from flask import Blueprint
from controllers.auth_controller import register, login, verify_email, testmiddleware, reset_password, verify_reset_password

auth_routes = Blueprint("auth", __name__)

auth_routes.route("/register", methods=["POST"])(register)
auth_routes.route("/login", methods=["POST"])(login)
auth_routes.route("/verify-email", methods=["GET"])(verify_email)
auth_routes.route("/reset-password", methods=["POST"])(reset_password)
auth_routes.route("/verify-reset-password", methods=["POST"])(verify_reset_password)
auth_routes.route("/me", methods=["GET"])(testmiddleware) #test