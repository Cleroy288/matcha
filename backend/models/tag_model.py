import psycopg2.extras
from database.db import get_connection


def create_tag(name):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        INSERT INTO tags (name) VALUES (%s)
        ON CONFLICT (name) DO NOTHING
    """, (name,))
    conn.commit()

    cur.execute("SELECT * FROM tags WHERE name = %s", (name,))
    tag = cur.fetchone()

    cur.close()
    conn.close()

    return dict(tag) if tag else None


def search_tags(query):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute(
        "SELECT * FROM tags WHERE name ILIKE %s ORDER BY name LIMIT 20",
        (f"%{query}%",)
    )
    tags = cur.fetchall()

    cur.close()
    conn.close()

    return [dict(t) for t in tags]


def get_all_tags():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT * FROM tags ORDER BY name")
    tags = cur.fetchall()

    cur.close()
    conn.close()

    return [dict(t) for t in tags]


def add_tag_to_user(user_id, tag_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO user_tags (user_id, tag_id) VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """, (user_id, tag_id))

    conn.commit()
    cur.close()
    conn.close()


def remove_tag_from_user(user_id, tag_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM user_tags WHERE user_id = %s AND tag_id = %s",
        (user_id, tag_id)
    )

    conn.commit()
    cur.close()
    conn.close()


def get_user_tags(user_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT t.id, t.name FROM tags t
        JOIN user_tags ut ON t.id = ut.tag_id
        WHERE ut.user_id = %s
        ORDER BY t.name
    """, (user_id,))
    tags = cur.fetchall()

    cur.close()
    conn.close()

    return [dict(t) for t in tags]


def count_user_tags(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM user_tags WHERE user_id = %s", (user_id,))
    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return count
