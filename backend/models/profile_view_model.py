from database.db import get_connection

def add_view(viewer_id, viewed_id):
    if (viewer_id == viewed_id):
        return 
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO profile_views (viewer_id; viewed_id)
        VALUES (%s, %s)
    """, (viewer_id, viewed_id))

    conn.commit()
    cur.close()
    conn.close()

def get_views_received(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT u.id, u.username, u.first_name, u.last_name, pv.viewed_at
        FROM profile_views pv
        JOIN users u ON u.id = pv_viewer_id
        WHERE pv.viewed_id = %s
        ORDER BY pv.viewed_at DESC
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [dict(zip(["id", "username", "first_name", "last_name", "viewed_at"], r)) for r in rows]