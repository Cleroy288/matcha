from database.db import get_connection


def recalculate_fame():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT recalculate_fame_ratings()")
        conn.commit()
    finally:
        cur.close()
        conn.close()