from flask import jsonify, request

from controllers.constants import HTTP_BAD_REQUEST, HTTP_OK
from services.browse_service import browse_suggestions, search_profiles
from utils.jwt_required import jwt_required


@jwt_required
def browse(payload):
    """GET /browse — profils suggérés (tri/filtres via query params)."""
    try:
        profiles = browse_suggestions(payload["user_id"], request.args)
        return jsonify({"profiles": profiles}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST


@jwt_required
def search(payload):
    """GET /search — recherche avancée (âge, fame, localisation, tags)."""
    try:
        profiles = search_profiles(payload["user_id"], request.args)
        return jsonify({"profiles": profiles}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST
