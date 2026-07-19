from models.browse_model import SORT_EXPRESSIONS, fetch_candidates
from models.profile_model import get_profile_by_user_id
from services.constants import BROWSE_DEFAULT_LIMIT, BROWSE_MAX_LIMIT
from services.errors import ERR_INVALID_FILTER, ERR_PROFILE_INCOMPLETE
from utils.photo_url import build_photo_url


def browse_suggestions(user_id, raw_params):
    """Liste de profils suggérés pour le feed : compatibles, non likés, non bloqués,
    triés par score (tags communs + proximité + fame) par défaut."""
    criteria = parse_criteria(raw_params)
    criteria["exclude_liked"] = True
    return run_candidates_query(user_id, criteria)


def search_profiles(user_id, raw_params):
    """Recherche avancée : mêmes candidats compatibles, critères explicites
    (tranche d'âge, plage de fame, localisation, tags), profils likés inclus."""
    criteria = parse_criteria(raw_params)
    criteria["exclude_liked"] = False
    criteria["tags"] = parse_tags(raw_params.get("tags"))
    return run_candidates_query(user_id, criteria)


def run_candidates_query(user_id, criteria):
    """Charge mon profil (préférences + position) puis exécute la requête candidates."""
    me = get_profile_by_user_id(user_id)
    if not me or not me.get("profile_complete"):
        raise Exception(ERR_PROFILE_INCOMPLETE)
    me["id"] = user_id

    candidates = fetch_candidates(me, criteria)
    for candidate in candidates:
        candidate["photo_urls"] = [
            build_photo_url(path)
            for path in candidate.pop("photo_paths", [])
            if path
        ]
        candidate["profile_photo_url"] = build_photo_url(candidate.pop("profile_photo"))
    return candidates


# ── Parsing des paramètres de requête ──

def parse_criteria(raw_params):
    """Valide et convertit les filtres communs navigation / recherche."""
    criteria = {
        "age_min": parse_number(raw_params.get("age_min"), int),
        "age_max": parse_number(raw_params.get("age_max"), int),
        "fame_min": parse_number(raw_params.get("fame_min"), float),
        "fame_max": parse_number(raw_params.get("fame_max"), float),
        "distance_max": parse_number(raw_params.get("distance_max"), float),
        "min_common_tags": parse_number(raw_params.get("min_common_tags"), int),
        "city": (raw_params.get("city") or "").strip() or None,
        "sort_by": parse_sort_by(raw_params.get("sort_by")),
        "order": raw_params.get("order"),
        "tags": None,
    }
    criteria["limit"] = parse_limit(raw_params.get("limit"))
    criteria["offset"] = parse_number(raw_params.get("offset"), int) or 0
    return criteria


def parse_number(value, cast):
    """Convertit un paramètre numérique optionnel ; vide = absent, invalide = erreur."""
    if value is None or value == "":
        return None
    try:
        return cast(value)
    except (ValueError, TypeError):
        raise Exception(ERR_INVALID_FILTER) from None


def parse_sort_by(value):
    """N'accepte que les tris whitelistés par le model."""
    if value is None or value == "":
        return None
    if value not in SORT_EXPRESSIONS:
        raise Exception(ERR_INVALID_FILTER)
    return value


def parse_limit(value):
    """Limite de pagination bornée."""
    limit = parse_number(value, int) or BROWSE_DEFAULT_LIMIT
    return max(1, min(limit, BROWSE_MAX_LIMIT))


def parse_tags(value):
    """Liste de tags de recherche : chaîne 'a,b,c' → liste nettoyée, None si vide."""
    if not value:
        return None
    tags = [tag.strip() for tag in value.split(",") if tag.strip()]
    return tags or None
