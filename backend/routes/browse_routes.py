from flask import Blueprint

from controllers.browse_controller import browse, search

browse_routes = Blueprint("browse", __name__)

# Navigation (suggestions) + recherche avancée
browse_routes.route("/browse", methods=["GET"])(browse)
browse_routes.route("/search", methods=["GET"])(search)
