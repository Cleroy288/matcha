import logging

from flask import jsonify, request
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)

HTTP_INTERNAL_SERVER_ERROR = 500

# Message générique : le détail d'un bug interne ne sort jamais vers le client,
# il part dans les logs serveur.
ERR_INTERNAL = "Internal server error"

# Descriptions Werkzeug remplacées par des messages courts et exploitables par le front.
ERROR_MESSAGES = {
    400: "Malformed request",
    404: "Resource not found",
    405: "Method not allowed",
    413: "Uploaded file is too large",
    415: "Request body must be JSON",
}


def register_error_handlers(app):
    """Garantit qu'aucune réponse d'erreur ne sort en HTML.

    Sans ces handlers, Flask sert ses pages d'erreur Werkzeug (404, 405, 413 sur
    MAX_CONTENT_LENGTH, 415 sur Content-Type manquant, 500) : le front appelle
    res.json() dessus et lève une SyntaxError."""

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        message = ERROR_MESSAGES.get(error.code, error.description)
        return jsonify({"error": message}), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_exception(error):
        # la stacktrace complète part dans les logs, jamais vers le client
        logger.exception("Unhandled exception on %s %s", request.method, request.path)
        return jsonify({"error": ERR_INTERNAL}), HTTP_INTERNAL_SERVER_ERROR
