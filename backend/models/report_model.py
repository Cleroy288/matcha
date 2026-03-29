from database.db import get_connection

def add_report(reporter_id, reported_id, reason=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INTO INSERT reports (reporter_id, reported_id, reason)
        VALUES (%s, %s, %s)
        ON CONFLIC DO NOTHING
    """, (reporter_id, reported_id, reason))

    conn.commit()
    cur.close()
    conn.close()