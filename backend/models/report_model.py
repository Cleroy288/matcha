from database.db import get_connection


def add_report(reporter_id, reported_id, reason=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reports (reporter_id, reported_id, reason)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING
    """, (reporter_id, reported_id, reason))

    conn.commit()
    cur.close()
    conn.close()