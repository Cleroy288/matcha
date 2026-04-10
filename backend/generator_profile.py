from faker import Faker
import random
from datetime import date, timedelta
from database.db import get_connection
from werkzeug.security import generate_password_hash

fake = Faker()

def random_birthdate(min_age=18, max_age=70):
    today = date.today()
    age = random.randint(min_age, max_age)
    return today - timedelta(days=age * 365)

def generate_users(n=500):
    conn = get_connection()
    cur = conn.cursor()

    for _ in range(n):
        # --- USERS ---
        email = fake.unique.email()
        username = fake.unique.user_name()
        password_hash = generate_password_hash("test123")

        first_name = fake.first_name()
        last_name = fake.last_name()

        email_verified = True
        verification_token = None

        cur.execute("""
            INSERT INTO users (
                email, username, password_hash,
                first_name, last_name,
                email_verified, verification_token
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            email, username, password_hash,
            first_name, last_name,
            email_verified, verification_token
        ))

        user_id = cur.fetchone()[0]

        birth_date = random_birthdate()
        biography = fake.text(max_nb_chars=200)
        city = fake.city()
        latitude = float(fake.latitude())
        longitude = float(fake.longitude())

        gender = random.choice(["male", "female"])
        sexual_preference = random.choice(["male", "female", "both"])
        fame_rating = random.randint(0, 10)

        cur.execute("""
            INSERT INTO profiles (
                user_id,
                gender, sexual_preference, biography, birth_date,
                fame_rating,
                latitude, longitude, city,
                gps_consent, profile_complete
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id,
            gender, sexual_preference, biography, birth_date,
            fame_rating,
            latitude, longitude, city,
            True, True
        ))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    generate_users(500)