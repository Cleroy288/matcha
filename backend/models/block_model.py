from database.db import get_connection

def add_block(blocker_id, blocked_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO blocks (blocker_id, blocked_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """, (blocker_id, blocked_id))
    conn.commit()
    cur.close()
    conn.close()

def remove_block(blocker_id, blocked_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM blocks WHERE blocker_id = %s AND blocked_id = %s
    """, (blocker_id, blocked_id))
    conn.commit()
    cur.close()
    conn.close()

def is_blocked(blocker_id, blocked_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT EXISTS (
            SELECT 1 FROM blocks
            WHERE (blocker_id = %s AND blocked_id = %s)
            OR    (blocker_id = %s AND blocked_id = %s)
        )
    """, (blocker_id, blocked_id, blocked_id, blocker_id))
    result = cur.fetchone()[0]
    cur.close()
    conn.close()
    return result