import psycopg2.extras

from database.db import get_connection


def create_message(sender_id, receiver_id, content):
    """Insère un message et retourne la ligne créée."""
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        INSERT INTO messages (sender_id, receiver_id, content)
        VALUES (%s, %s, %s)
        RETURNING *
    """, (sender_id, receiver_id, content))
    message = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return dict(message) if message else None


def get_conversation_messages(user_id, other_id, limit):
    """Derniers messages échangés entre les deux users, du plus ancien au plus récent."""
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT * FROM (
            SELECT * FROM messages
            WHERE (sender_id = %(me)s AND receiver_id = %(other)s)
               OR (sender_id = %(other)s AND receiver_id = %(me)s)
            ORDER BY created_at DESC, id DESC
            LIMIT %(limit)s
        ) AS latest
        ORDER BY created_at ASC, id ASC
    """, {"me": user_id, "other": other_id, "limit": limit})
    messages = cur.fetchall()

    cur.close()
    conn.close()

    return [dict(m) for m in messages]


def mark_conversation_read(user_id, other_id):
    """Marque comme lus les messages reçus de other_id."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE messages SET is_read = TRUE
        WHERE sender_id = %s AND receiver_id = %s AND is_read = FALSE
    """, (other_id, user_id))

    conn.commit()
    cur.close()
    conn.close()


def count_unread_messages(user_id):
    """Nombre total de messages non lus (badge toutes pages)."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM messages WHERE receiver_id = %s AND is_read = FALSE",
        (user_id,)
    )
    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return count


def get_conversations(user_id):
    """Liste des matchs (likes mutuels, non bloqués) avec dernier message,
    compteur de non-lus et statut en ligne, triée par activité récente."""
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        WITH matches AS (
            SELECT l1.liked_id AS other_id
            FROM likes l1
            JOIN likes l2 ON l2.liker_id = l1.liked_id AND l2.liked_id = l1.liker_id
            WHERE l1.liker_id = %(me)s
        )
        SELECT
            m.other_id AS user_id,
            u.username, u.first_name, u.last_name,
            p.is_online, p.last_online,
            (SELECT ph.file_path FROM photos ph
                WHERE ph.user_id = m.other_id AND ph.is_profile = TRUE LIMIT 1) AS profile_photo,
            lm.content    AS last_message,
            lm.created_at AS last_message_at,
            lm.sender_id  AS last_sender_id,
            (SELECT COUNT(*) FROM messages msg
                WHERE msg.sender_id = m.other_id AND msg.receiver_id = %(me)s
                  AND msg.is_read = FALSE)::int AS unread_count
        FROM matches m
        JOIN users u ON u.id = m.other_id
        LEFT JOIN profiles p ON p.user_id = m.other_id
        LEFT JOIN LATERAL (
            SELECT content, created_at, sender_id FROM messages
            WHERE (sender_id = m.other_id AND receiver_id = %(me)s)
               OR (sender_id = %(me)s AND receiver_id = m.other_id)
            ORDER BY created_at DESC, id DESC
            LIMIT 1
        ) lm ON TRUE
        WHERE NOT EXISTS (
            SELECT 1 FROM blocks b
            WHERE (b.blocker_id = %(me)s AND b.blocked_id = m.other_id)
               OR (b.blocker_id = m.other_id AND b.blocked_id = %(me)s)
        )
        ORDER BY lm.created_at DESC NULLS LAST, u.username ASC
    """, {"me": user_id})
    conversations = cur.fetchall()

    cur.close()
    conn.close()

    return [dict(c) for c in conversations]
