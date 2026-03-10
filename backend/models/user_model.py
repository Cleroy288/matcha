from database.db import get_connection


def create_user(email, username, password_hash, first_name, last_name):

    conn = get_connection()
    cur = conn.cursor()

    query = """
    INSERT INTO users (email, username, password_hash, first_name, last_name)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id
    """

    cur.execute(query, (email, username, password_hash, first_name, last_name))

    user_id = cur.fetchone()[0]

    conn.commit()

    cur.close()
    conn.close()

    return user_id

def get_user_by_email(email):
    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT id, email, username FROM users
    WHERE email = %s
    """
    cur.execute(query, (email,))

    user = cur.fetchone()

    cur.close()
    conn.close()

    if user:
        return {
            "id": user[0],
            "email": user[1],
            "username": user[2]
        }

    return None

def get_user_by_username(username):
    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT id, email, username, password_hash FROM users
    WHERE username = %s
    """
    cur.execute(query, (username,))

    user = cur.fetchone()

    cur.close()
    conn.close()

    if user:
        return {
            "id": user[0],
            "email": user[1],
            "username": user[2],
            "password_hash": user[3]
        }

    return None
