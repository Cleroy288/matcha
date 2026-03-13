import psycopg2.extras
from database.db import get_connection

def create_user(email, username, password_hash, first_name, last_name, token):

    conn = get_connection()
    cur = conn.cursor()

    query = """
    INSERT INTO users (email, username, password_hash, first_name, last_name, verification_token)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING id
    """

    cur.execute(query, (email, username, password_hash, first_name, last_name, token))

    user_id = cur.fetchone()[0]

    conn.commit()

    cur.close()
    conn.close()

    return user_id

def get_user_by_email(email):
    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT id, email, username, first_name, last_name, email_verified FROM users
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
            "username": user[2],
            "first_name": user[3],
            "last_name": user[4],
            "email_verified": user[5]
        }

    return None

def get_user_by_username(username):
    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT id, email, username, password_hash, first_name, last_name, email_verified FROM users
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
            "password_hash": user[3],
            "first_name": user[4],
            "last_name": user[5],
            "email_verified": user[6]
        }

    return None

def get_user_by_id(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    cur.execute("SELECT id, email, username, first_name, last_name FROM users WHERE id = %s", (id,))
    user = cur.fetchone()

    cur.close()
    conn.close()

    return user

def get_user_by_verification_token(token):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id FROM users WHERE verification_token = %s", (token,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

def set_new_password(password_hash, token):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id FROM users WHERE verification_token = %s", (token,))
    user = cur.fetchone()
    if user:
        cur.execute("UPDATE users  SET password_hash = %s, verification_token = NULL WHERE id = %s", (password_hash, user['id'],))
        conn.commit()
    cur.close()
    conn.close()
    return user

def confirm_user_email(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users 
        SET email_verified = TRUE, verification_token = NULL 
        WHERE id = %s
    """, (user_id,))
    conn.commit()
    cur.close()
    conn.close()

def set_token_reset_password_user_email(email, token):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users 
        SET verification_token = %s
        WHERE email = %s
    """, (token, email,))
    conn.commit()
    cur.close()
    conn.close()