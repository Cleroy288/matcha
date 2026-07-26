from flask import request

from utils.app_error import AppError

ERR_UNREADABLE_JSON_BODY = "Request body must be valid JSON with Content-Type: application/json"
ERR_INVALID_JSON_BODY = "Request body must be a JSON object"
ERR_MISSING_FIELD = "Missing or empty required field: {field}"


def get_json_body():
    """Corps JSON de la requête, sans jamais laisser Werkzeug lever un 415/400.

    request.json lève UnsupportedMediaType dès que le Content-Type n'est pas
    application/json, et BadRequest sur un JSON malformé : deux erreurs que le
    client déclenche trivialement, et que Flask rendait en HTML. On les convertit
    en AppError, tout en distinguant les trois cas pour que le message reste
    exploitable : corps absent, corps illisible, corps qui n'est pas un objet."""
    body = request.get_json(silent=True)
    if body is None:
        # un corps a bien été envoyé mais n'a pas pu être lu : mauvais
        # Content-Type ou JSON malformé — le signaler plutôt que de le confondre
        # avec des champs manquants
        if request.get_data():
            raise AppError(ERR_UNREADABLE_JSON_BODY)
        return {}
    if not isinstance(body, dict):
        raise AppError(ERR_INVALID_JSON_BODY)
    return body


def require_fields(body, *fields):
    """Vérifie que chaque champ est présent et vaut une chaîne non vide.

    Évite à la fois les KeyError des contrôleurs et les TypeError des
    validateurs (validate_email fait len(email) sans typer son entrée)."""
    for field in fields:
        value = body.get(field)
        if not isinstance(value, str) or not value.strip():
            raise AppError(ERR_MISSING_FIELD.format(field=field))
