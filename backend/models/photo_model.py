import psycopg2.extras

from database.db import get_connection


def create_photo(user_id, file_path, is_profile, sort_order):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        INSERT INTO photos (user_id, file_path, is_profile, sort_order)
        VALUES (%s, %s, %s, %s) RETURNING *
    """, (user_id, file_path, is_profile, sort_order))
    photo = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return dict(photo) if photo else None


def get_photos_by_user(user_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute(
        "SELECT * FROM photos WHERE user_id = %s ORDER BY sort_order",
        (user_id,)
    )
    photos = cur.fetchall()

    cur.close()
    conn.close()

    return [dict(p) for p in photos]


def get_photo_by_id(photo_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT * FROM photos WHERE id = %s", (photo_id,))
    photo = cur.fetchone()

    cur.close()
    conn.close()

    return dict(photo) if photo else None


def count_user_photos(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM photos WHERE user_id = %s", (user_id,))
    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return count


def delete_photo(photo_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("DELETE FROM photos WHERE id = %s RETURNING file_path", (photo_id,))
    result = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return dict(result) if result else None


def set_profile_photo(user_id, photo_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE photos SET is_profile = FALSE WHERE user_id = %s",
        (user_id,)
    )
    cur.execute(
        "UPDATE photos SET is_profile = TRUE WHERE id = %s AND user_id = %s",
        (photo_id, user_id)
    )

    conn.commit()
    cur.close()
    conn.close()


def get_profile_photo(user_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute(
        "SELECT * FROM photos WHERE user_id = %s AND is_profile = TRUE",
        (user_id,)
    )
    photo = cur.fetchone()

    cur.close()
    conn.close()

    return dict(photo) if photo else None
