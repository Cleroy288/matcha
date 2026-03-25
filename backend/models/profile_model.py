import psycopg2.extras
from database.db import get_connection
from models.constants import PROFILE_ALLOWED_FIELDS


def create_profile(user_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute(
        "INSERT INTO profiles (user_id) VALUES (%s) RETURNING *",
        (user_id,)
    )
    profile = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return dict(profile) if profile else None


def get_profile_by_user_id(user_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT * FROM profiles WHERE user_id = %s", (user_id,))
    profile = cur.fetchone()

    cur.close()
    conn.close()

    return dict(profile) if profile else None


def update_profile(user_id, fields):
    safe_fields = {k: v for k, v in fields.items() if k in PROFILE_ALLOWED_FIELDS}
    if not safe_fields:
        return None

    set_clause = ", ".join(f"{k} = %s" for k in safe_fields)
    values = list(safe_fields.values())
    values.append(user_id)

    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    query = f"UPDATE profiles SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE user_id = %s RETURNING *"
    cur.execute(query, values)
    profile = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return dict(profile) if profile else None


def update_location(user_id, lat, lng, city, gps_consent):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        UPDATE profiles
        SET latitude = %s, longitude = %s, city = %s, gps_consent = %s, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = %s RETURNING *
    """, (lat, lng, city, gps_consent, user_id))
    profile = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return dict(profile) if profile else None


def set_profile_complete(user_id, is_complete):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE profiles SET profile_complete = %s, updated_at = CURRENT_TIMESTAMP WHERE user_id = %s",
        (is_complete, user_id)
    )

    conn.commit()
    cur.close()
    conn.close()
