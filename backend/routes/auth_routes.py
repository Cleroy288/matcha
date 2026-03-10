from flask import Blueprint
from controllers.auth_controller import register, login, testmiddleware

auth_routes = Blueprint("auth", __name__)

auth_routes.route("/register", methods=["POST"])(register)
auth_routes.route("/login", methods=["POST"])(login)
auth_routes.route("/me", methods=["GET"])(testmiddleware) #test