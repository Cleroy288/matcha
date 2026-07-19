import argparse
import os
import random
import uuid
from io import BytesIO
from urllib.error import URLError
from urllib.request import Request, urlopen

import bcrypt
from faker import Faker
from PIL import Image

from database.db import get_connection
from services.constants import MIN_TAGS_FOR_COMPLETE, UPLOAD_DIR

fake = Faker()

# Shared intentionally: these accounts only exist as local evaluation data.
SEED_PASSWORD = "Zxqv9!mN482"
SEED_PHOTOS_PER_USER = 2
MAX_REMOTE_IMAGE_SIZE = 5 * 1024 * 1024
PORTRAIT_URL = "https://randomuser.me/api/portraits/{category}/{index}.jpg"
TAG_NAMES = (
    "#art",
    "#books",
    "#cinema",
    "#coffee",
    "#cooking",
    "#fitness",
    "#gaming",
    "#geek",
    "#hiking",
    "#music",
    "#nature",
    "#photography",
    "#sports",
    "#travel",
    "#vegan",
)
AVATAR_COLORS = (
    "#2F6BFF",
    "#FF5C8A",
    "#2EAD73",
    "#F2B134",
    "#7C4DFF",
    "#E4572E",
)

VALID_PROFILE_COUNT_SQL = f"""
    SELECT COUNT(*)
    FROM profiles p
    WHERE p.profile_complete = TRUE
      AND p.gender IS NOT NULL
      AND p.sexual_preference IS NOT NULL
      AND NULLIF(BTRIM(p.biography), '') IS NOT NULL
      AND p.birth_date IS NOT NULL
      AND (
          (p.gps_consent = TRUE AND p.latitude IS NOT NULL AND p.longitude IS NOT NULL)
          OR NULLIF(BTRIM(p.city), '') IS NOT NULL
      )
      AND (SELECT COUNT(*) FROM user_tags ut WHERE ut.user_id = p.user_id) >= {MIN_TAGS_FOR_COMPLETE}
      AND EXISTS (
          SELECT 1 FROM photos ph
          WHERE ph.user_id = p.user_id AND ph.is_profile = TRUE
      )
"""


def generate_users(target=500):
    conn = get_connection()
    cur = conn.cursor()
    created_files = []
    replaced_files = []

    try:
        cur.execute(VALID_PROFILE_COUNT_SQL)
        missing = max(0, target - cur.fetchone()[0])

        if missing:
            tag_ids = ensure_tags(cur)
            password_hash = bcrypt.hashpw(SEED_PASSWORD.encode(), bcrypt.gensalt()).decode()

            for _ in range(missing):
                user_id = create_seed_user(cur, password_hash)
                create_seed_profile(cur, user_id)
                for tag_id in random.sample(tag_ids, random.randint(MIN_TAGS_FOR_COMPLETE, 8)):
                    cur.execute(
                        "INSERT INTO user_tags (user_id, tag_id) VALUES (%s, %s)",
                        (user_id, tag_id),
                    )

        os.makedirs(UPLOAD_DIR, exist_ok=True)
        updated_galleries, fallback_count = ensure_seed_galleries(cur, created_files, replaced_files)

        cur.execute(VALID_PROFILE_COUNT_SQL)
        if cur.fetchone()[0] < target:
            raise RuntimeError("Seed validation failed")

        conn.commit()
        remove_replaced_files(replaced_files)
        return missing, updated_galleries, fallback_count
    except Exception:
        conn.rollback()
        remove_created_files(created_files)
        raise
    finally:
        cur.close()
        conn.close()


def ensure_tags(cur):
    tag_ids = []
    for name in TAG_NAMES:
        cur.execute(
            """
            INSERT INTO tags (name) VALUES (%s)
            ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
            RETURNING id
            """,
            (name,),
        )
        tag_ids.append(cur.fetchone()[0])
    return tag_ids


def create_seed_user(cur, password_hash):
    key = uuid.uuid4().hex
    cur.execute(
        """
        INSERT INTO users (
            email, username, password_hash, first_name, last_name,
            email_verified, verification_token
        )
        VALUES (%s, %s, %s, %s, %s, TRUE, NULL)
        RETURNING id
        """,
        (
            f"seed_{key}@matcha.test",
            f"seed_{key[:16]}",
            password_hash,
            fake.first_name(),
            fake.last_name(),
        ),
    )
    return cur.fetchone()[0]


def create_seed_profile(cur, user_id):
    cur.execute(
        """
        INSERT INTO profiles (
            user_id, gender, sexual_preference, biography, birth_date,
            fame_rating, latitude, longitude, city, gps_consent, profile_complete
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE, TRUE)
        """,
        (
            user_id,
            random.choice(("male", "female", "other")),
            random.choice(("male", "female", "bisexual")),
            fake.text(max_nb_chars=240),
            fake.date_of_birth(minimum_age=18, maximum_age=70),
            random.randint(0, 10),
            float(fake.latitude()),
            float(fake.longitude()),
            fake.city(),
        ),
    )


def ensure_seed_galleries(cur, created_files, replaced_files):
    cur.execute(
        """
        SELECT u.id, p.gender
        FROM users u
        JOIN profiles p ON p.user_id = u.id
        WHERE u.email LIKE 'seed_%@matcha.test'
        ORDER BY u.id
        """
    )
    seed_users = cur.fetchall()
    portrait_cache = {}
    updated = 0
    fallback_count = 0

    for user_id, gender in seed_users:
        cur.execute(
            "SELECT file_path, is_profile FROM photos WHERE user_id = %s ORDER BY sort_order, id",
            (user_id,),
        )
        current_photos = cur.fetchall()
        if gallery_is_ready(current_photos):
            continue

        new_filenames = []
        for slot in range(SEED_PHOTOS_PER_USER):
            filename = f"seed_{user_id}_{slot}_{uuid.uuid4().hex[:8]}.jpg"
            path = os.path.join(UPLOAD_DIR, filename)
            used_fallback = save_seed_portrait(path, user_id, gender, slot, portrait_cache)
            fallback_count += int(used_fallback)
            created_files.append(path)
            new_filenames.append(filename)

        cur.execute("DELETE FROM photos WHERE user_id = %s", (user_id,))
        for sort_order, filename in enumerate(new_filenames):
            cur.execute(
                """
                INSERT INTO photos (user_id, file_path, is_profile, sort_order)
                VALUES (%s, %s, %s, %s)
                """,
                (user_id, filename, sort_order == 0, sort_order),
            )

        replaced_files.extend(safe_seed_paths(photo[0] for photo in current_photos))
        updated += 1

    return updated, fallback_count


def gallery_is_ready(photos):
    if len(photos) < SEED_PHOTOS_PER_USER or not any(photo[1] for photo in photos):
        return False
    return all(os.path.exists(os.path.join(UPLOAD_DIR, photo[0])) for photo in photos)


def save_seed_portrait(path, user_id, gender, slot, cache):
    category = portrait_category(gender, user_id, slot)
    portrait_index = (user_id * SEED_PHOTOS_PER_USER + slot) % 100
    cache_key = (category, portrait_index)

    if cache_key not in cache:
        cache[cache_key] = download_portrait(category, portrait_index)

    data = cache[cache_key]
    if data is None:
        Image.new("RGB", (512, 512), random.choice(AVATAR_COLORS)).save(path, "JPEG", quality=90)
        return True

    with Image.open(BytesIO(data)) as source:
        image = source.convert("RGB").resize((512, 512), Image.Resampling.LANCZOS)
        image.save(path, "JPEG", quality=90)
    return False


def portrait_category(gender, user_id, slot):
    if gender == "female":
        return "women"
    if gender == "male":
        return "men"
    return "women" if (user_id + slot) % 2 else "men"


def download_portrait(category, index):
    request = Request(
        PORTRAIT_URL.format(category=category, index=index),
        headers={"User-Agent": "Matcha seed generator"},
    )
    try:
        with urlopen(request, timeout=10) as response:
            data = response.read(MAX_REMOTE_IMAGE_SIZE + 1)
        if len(data) > MAX_REMOTE_IMAGE_SIZE:
            return None
        with Image.open(BytesIO(data)) as image:
            image.verify()
        return data
    except (OSError, URLError, ValueError):
        return None


def safe_seed_paths(filenames):
    return [
        os.path.join(UPLOAD_DIR, filename)
        for filename in filenames
        if filename == os.path.basename(filename) and filename.startswith("seed_")
    ]


def remove_created_files(paths):
    for path in paths:
        if os.path.exists(path):
            os.remove(path)


def remove_replaced_files(paths):
    for path in paths:
        try:
            os.remove(path)
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create valid Matcha seed profiles")
    parser.add_argument("count", nargs="?", type=int, default=500, help="target number of valid profiles")
    args = parser.parse_args()

    if args.count < 1:
        parser.error("count must be at least 1")

    created, updated, fallbacks = generate_users(args.count)
    print(f"Created {created} profiles; target: {args.count}")
    print(f"Updated {updated} seed galleries ({SEED_PHOTOS_PER_USER} photos each, {fallbacks} fallbacks)")
    print(f"Seed account password: {SEED_PASSWORD}")
