from database.db import get_connection

def create_notification(user_id, from_user_id, notif_type):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO notifications (user_id, from_user_id, type)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (user_id, from_user_id, notif_type))
    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return result[0]

def get_notifications(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT n.id, n.type, n.is_read, n.created_at,
               u.username, u.first_name, u.last_name
        FROM notifications n
        LEFT JOIN users u ON u.id = n.from_user_id
        WHERE n.user_id = %s
        ORDER BY n.created_at DESC
        LIMIT 50
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(zip(
        ["id", "type", "is_read", "created_at", "username", "first_name", "last_name"], r
    )) for r in rows]

def mark_all_read(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE notifications SET is_read = TRUE
        WHERE user_id = %s AND is_read = FALSE
    """, (user_id,))
    conn.commit()
    cur.close()
    conn.close()

def count_unread(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM notifications
        WHERE user_id = %s AND is_read = FALSE
    """, (user_id,))
    result = cur.fetchone()[0]
    cur.close()
    conn.close()
    return result