import psycopg2.extras

from database.db import get_connection
from services.constants import (
    SUGGESTION_FAR_DISTANCE_KM,
    SUGGESTION_PROXIMITY_POINTS_PER_KM,
    SUGGESTION_PROXIMITY_RADIUS_KM,
    SUGGESTION_WEIGHT_COMMON_TAG,
    SUGGESTION_WEIGHT_FAME,
    SUGGESTION_WEIGHT_SAME_CITY,
)

# Allowed sorts (key exposed to the API → SQL expression on the candidates subquery)
SORT_EXPRESSIONS = {
    "score":       "score",
    "age":         "age",
    "distance":    "distance_km",
    "fame":        "fame_rating",
    "common_tags": "common_tags",
}


def fetch_candidates(me, criteria):
    """Returns the profiles compatible with `me`, filtered/sorted by `criteria`.

    me       : {id, gender, sexual_preference, latitude, longitude}
    criteria : {age_min, age_max, fame_min, fame_max, distance_max, city,
                min_common_tags, tags, exclude_liked, sort_by, order, limit, offset}
    """
    params = build_base_params(me, criteria)
    inner_where = build_inner_where(criteria)
    outer_where = build_outer_where(criteria, params)
    order_clause = build_order_clause(criteria)

    query = f"""
        SELECT * FROM (
            SELECT
                u.id AS user_id,
                u.username, u.first_name, u.last_name,
                p.gender, p.sexual_preference, p.city,
                p.fame_rating::float AS fame_rating,
                p.is_online, p.last_online,
                CASE WHEN NULLIF(BTRIM(%(me_city)s::text), '') IS NOT NULL
                           AND LOWER(BTRIM(p.city)) = LOWER(BTRIM(%(me_city)s::text))
                     THEN 1 ELSE 0 END AS same_city,
                DATE_PART('year', AGE(p.birth_date))::int AS age,
                (SELECT ph.file_path FROM photos ph
                    WHERE ph.user_id = u.id AND ph.is_profile = TRUE LIMIT 1) AS profile_photo,
                ARRAY(SELECT ph.file_path FROM photos ph
                    WHERE ph.user_id = u.id
                    ORDER BY ph.is_profile DESC, ph.sort_order, ph.id) AS photo_paths,
                (SELECT COUNT(*) FROM user_tags ut
                    JOIN user_tags mt ON mt.tag_id = ut.tag_id AND mt.user_id = %(me_id)s
                    WHERE ut.user_id = u.id)::int AS common_tags,
                {DISTANCE_SQL} AS distance_km
            FROM users u
            JOIN profiles p ON p.user_id = u.id
            WHERE u.id != %(me_id)s
              AND p.profile_complete = TRUE
              AND (
                    (p.gps_consent = TRUE
                     AND p.latitude IS NOT NULL
                     AND p.longitude IS NOT NULL)
                    OR NULLIF(BTRIM(p.city), '') IS NOT NULL
              )
              AND p.gender IS NOT NULL
              AND p.birth_date IS NOT NULL
              AND (%(me_pref)s NOT IN ('male', 'female') OR p.gender = %(me_pref)s)
              AND (p.sexual_preference IS NULL
                   OR p.sexual_preference NOT IN ('male', 'female')
                   OR p.sexual_preference = %(me_gender)s)
              AND NOT EXISTS (SELECT 1 FROM blocks b
                    WHERE (b.blocker_id = %(me_id)s AND b.blocked_id = u.id)
                       OR (b.blocker_id = u.id AND b.blocked_id = %(me_id)s))
              {inner_where}
        ) AS candidates
        {outer_where}
        ORDER BY {order_clause}
        LIMIT %(limit)s OFFSET %(offset)s
    """

    return run_query(query, params)


# ── Query construction ──

# Haversine (km) between me and the candidate; NULL when either side has no position
DISTANCE_SQL = """
    CASE WHEN p.latitude IS NULL OR p.longitude IS NULL
              OR %(me_lat)s::float IS NULL OR %(me_lng)s::float IS NULL
    THEN NULL
    ELSE 6371 * acos(LEAST(1.0, GREATEST(-1.0,
        cos(radians(%(me_lat)s)) * cos(radians(p.latitude))
        * cos(radians(p.longitude) - radians(%(me_lng)s))
        + sin(radians(%(me_lat)s)) * sin(radians(p.latitude)))))
    END
"""

# Suggestion score: common tags + geographic proximity + fame
SCORE_SQL = f"""
    (common_tags * {SUGGESTION_WEIGHT_COMMON_TAG})
    + (fame_rating * {SUGGESTION_WEIGHT_FAME})
    + (same_city * {SUGGESTION_WEIGHT_SAME_CITY})
    + GREATEST(0, ({SUGGESTION_PROXIMITY_RADIUS_KM}
        - COALESCE(distance_km, {SUGGESTION_FAR_DISTANCE_KM}))
        * {SUGGESTION_PROXIMITY_POINTS_PER_KM})
"""


def build_base_params(me, criteria):
    """Builds the shared SQL params; missing preference = bisexual (subject IV.3)."""
    preference = me.get("sexual_preference") or "bisexual"
    return {
        "me_id": me["id"],
        "me_gender": me.get("gender"),
        "me_pref": preference,
        "me_lat": me.get("latitude"),
        "me_lng": me.get("longitude"),
        "me_city": me.get("city"),
        "limit": criteria["limit"],
        "offset": criteria["offset"],
    }


def build_inner_where(criteria):
    """Clauses that do not depend on the computed columns (likes already given)."""
    if not criteria.get("exclude_liked"):
        return ""
    return """AND NOT EXISTS (SELECT 1 FROM likes l
                WHERE l.liker_id = %(me_id)s AND l.liked_id = u.id)"""


def build_outer_where(criteria, params):
    """Filters on the computed columns: age, fame, distance, city, tags."""
    clauses = []
    append_range_filters(clauses, params, criteria)
    append_location_filters(clauses, params, criteria)
    append_tag_filters(clauses, params, criteria)

    if not clauses:
        return ""
    return "WHERE " + " AND ".join(clauses)


def append_range_filters(clauses, params, criteria):
    """Age range and fame range filters."""
    for key, clause in [
        ("age_min", "age >= %(age_min)s"),
        ("age_max", "age <= %(age_max)s"),
        ("fame_min", "fame_rating >= %(fame_min)s"),
        ("fame_max", "fame_rating <= %(fame_max)s"),
    ]:
        if criteria.get(key) is not None:
            params[key] = criteria[key]
            clauses.append(clause)


def append_location_filters(clauses, params, criteria):
    """Location filters: radius in km and/or city name."""
    if criteria.get("distance_max") is not None:
        params["distance_max"] = criteria["distance_max"]
        clauses.append("distance_km <= %(distance_max)s")

    if criteria.get("city"):
        params["city"] = f"%{criteria['city']}%"
        clauses.append("city ILIKE %(city)s")


def append_tag_filters(clauses, params, criteria):
    """Tag filters: minimum number of common tags, or a required tag list."""
    if criteria.get("min_common_tags") is not None:
        params["min_common_tags"] = criteria["min_common_tags"]
        clauses.append("common_tags >= %(min_common_tags)s")

    if criteria.get("tags"):
        params["tags"] = criteria["tags"]
        params["tags_count"] = len(criteria["tags"])
        clauses.append("""(SELECT COUNT(*) FROM user_tags ut
            JOIN tags t ON t.id = ut.tag_id
            WHERE ut.user_id = candidates.user_id AND t.name = ANY(%(tags)s)) = %(tags_count)s""")


def build_order_clause(criteria):
    """Whitelisted sort; suggestion score as default sort and tie-breaker."""
    sort_by = criteria.get("sort_by") or "score"
    expression = SORT_EXPRESSIONS.get(sort_by, "score")

    direction = "ASC" if criteria.get("order") == "asc" else "DESC"
    if sort_by in ("age", "distance") and criteria.get("order") != "desc":
        direction = "ASC"

    if expression == "score":
        return f"({SCORE_SQL}) {direction}, user_id ASC"
    return f"{expression} {direction} NULLS LAST, ({SCORE_SQL}) DESC, user_id ASC"


def run_query(query, params):
    """Runs the candidates query and serializes the rows."""
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute(query, params)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [dict(row) for row in rows]
