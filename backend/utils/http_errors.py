import logging

from flask import jsonify, request
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)

HTTP_INTERNAL_SERVER_ERROR = 500

# Generic message: the details of an internal bug never reach the client,
# they go to the server logs.
ERR_INTERNAL = "Internal server error"

# Werkzeug descriptions replaced by short messages the frontend can use.
ERROR_MESSAGES = {
    400: "Malformed request",
    404: "Resource not found",
    405: "Method not allowed",
    413: "Uploaded file is too large",
    415: "Request body must be JSON",
}


def register_error_handlers(app):
    """Guarantees that no error response is ever returned as HTML.

    Without these handlers Flask serves its Werkzeug error pages (404, 405, 413
    on MAX_CONTENT_LENGTH, 415 on a missing Content-Type, 500): the frontend
    calls res.json() on them and throws a SyntaxError."""

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        message = ERROR_MESSAGES.get(error.code, error.description)
        return jsonify({"error": message}), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_exception(error):
        # the full stacktrace goes to the logs, never to the client
        logger.exception("Unhandled exception on %s %s", request.method, request.path)
        return jsonify({"error": ERR_INTERNAL}), HTTP_INTERNAL_SERVER_ERROR
