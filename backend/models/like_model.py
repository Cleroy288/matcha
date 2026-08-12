import psycopg2.extras

from database.db import get_connection


def add_like(liker_id, liked_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO likes (liker_id, liked_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
        RETURNING id
    """, (liker_id, liked_id))

    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return result is not None

def remove_like(liker_id, liked_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM likes where liker_id = %s AND liked_id = %s
    """, (liker_id, liked_id))

    conn.commit()
    cur.close()
    conn.close()

def has_liked(liker_id, liked_id):
    """True if liker_id has already liked liked_id."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT EXISTS (SELECT 1 FROM likes WHERE liker_id = %s AND liked_id = %s)",
        (liker_id, liked_id)
    )
    result = cur.fetchone()[0]

    cur.close()
    conn.close()
    return result

def is_match(user1_id, user2_id):
    conn = get_connection()
    cur  = conn.cursor()

    cur.execute("""
        SELECT EXISTS (
            SELECT 1 FROM likes WHERE liker_id = %s AND liked_id = %s
        ) AND EXISTS (
            SELECT 1 FROM likes WHERE liker_id = %s AND liked_id = %s
        )
    """, (user1_id, user2_id, user2_id, user1_id))
    result = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return result

def get_likes_received(user_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT u.id, u.username, u.first_name, u.last_name,
               l.created_at AS liked_at
        FROM likes l
        JOIN users u ON u.id = l.liker_id
        WHERE l.liked_id = %s
        ORDER BY l.created_at DESC
    """, (user_id,))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(row) for row in rows]
