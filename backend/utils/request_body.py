from flask import request

from utils.app_error import AppError

ERR_UNREADABLE_JSON_BODY = "Request body must be valid JSON with Content-Type: application/json"
ERR_INVALID_JSON_BODY = "Request body must be a JSON object"
ERR_MISSING_FIELD = "Missing or empty required field: {field}"


def get_json_body():
    """JSON body of the request, without ever letting Werkzeug raise a 415/400.

    request.json raises UnsupportedMediaType as soon as the Content-Type is not
    application/json, and BadRequest on malformed JSON: two errors the client
    triggers trivially, and that Flask used to render as HTML. They are turned
    into AppError, keeping the three cases apart so the message stays usable:
    missing body, unreadable body, body that is not an object."""
    body = request.get_json(silent=True)
    if body is None:
        # a body was sent but could not be read: wrong Content-Type or
        # malformed JSON — report it rather than confusing it with
        # missing fields
        if request.get_data():
            raise AppError(ERR_UNREADABLE_JSON_BODY)
        return {}
    if not isinstance(body, dict):
        raise AppError(ERR_INVALID_JSON_BODY)
    return body


def require_fields(body, *fields):
    """Checks that every field is present and holds a non-empty string.

    Prevents both the KeyError in the controllers and the TypeError in the
    validators (validate_email calls len(email) without typing its input)."""
    for field in fields:
        value = body.get(field)
        if not isinstance(value, str) or not value.strip():
            raise AppError(ERR_MISSING_FIELD.format(field=field))
