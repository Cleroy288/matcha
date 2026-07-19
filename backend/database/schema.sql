CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,

    first_name VARCHAR(100),
    last_name VARCHAR(100),

    password_hash TEXT NOT NULL,

    email_verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    gender VARCHAR(10),
    sexual_preference VARCHAR(10),
    biography TEXT,
    birth_date DATE,

    fame_rating NUMERIC(4,1) DEFAULT 0,

    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    city VARCHAR(100),
    gps_consent BOOLEAN DEFAULT FALSE,

    last_online TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_online BOOLEAN DEFAULT FALSE,
    profile_complete BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE profiles ALTER COLUMN sexual_preference DROP DEFAULT;

CREATE TABLE IF NOT EXISTS tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS user_tags (
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, tag_id)
);

CREATE TABLE IF NOT EXISTS photos (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    file_path TEXT NOT NULL,
    is_profile BOOLEAN DEFAULT FALSE,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_photos_user_id ON photos(user_id);

CREATE TABLE IF NOT EXISTS likes (
    id          SERIAL PRIMARY KEY,
    liker_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    liked_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (liker_id, liked_id)
);

CREATE TABLE IF NOT EXISTS profile_views (
    id          SERIAL PRIMARY KEY,
    viewer_id   INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    viewed_id   INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    viewed_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS blocks (
    id          SERIAL PRIMARY KEY,
    blocker_id  INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    blocked_id  INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (blocker_id, blocked_id)
);

CREATE TABLE IF NOT EXISTS reports (
    id          SERIAL PRIMARY KEY,
    reporter_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reported_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reason      TEXT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (reporter_id, reported_id)
);

CREATE TABLE IF NOT EXISTS messages (
    id          SERIAL PRIMARY KEY,
    sender_id   INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    receiver_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content     TEXT NOT NULL,
    is_read     BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_messages_receiver ON messages(receiver_id, is_read);
CREATE INDEX IF NOT EXISTS idx_messages_pair ON messages(sender_id, receiver_id, created_at);

CREATE TABLE IF NOT EXISTS notifications (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    from_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    type        VARCHAR(20) NOT NULL,  -- 'like', 'visit', 'match', 'unlike', 'message'
    is_read     BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION recalculate_fame_ratings()
RETURNS VOID AS $$
DECLARE
    max_score NUMERIC;
BEGIN
    WITH scored AS (
        SELECT
            u.id AS user_id,
            GREATEST(
                (COUNT(DISTINCT l.id) * 3) +
                (COUNT(DISTINCT pv.id) * 1) -
                (COUNT(DISTINCT r.id) * 5),
            0) AS total
        FROM users u
        LEFT JOIN likes l         ON l.liked_id    = u.id
        LEFT JOIN profile_views pv ON pv.viewed_id  = u.id
        LEFT JOIN reports r        ON r.reported_id = u.id
        GROUP BY u.id
    )
    SELECT COALESCE(NULLIF(MAX(total), 0), 1) INTO max_score FROM scored;

    UPDATE profiles p
    SET fame_rating = ROUND(
        (s.total::NUMERIC / max_score) * 10, 1
    )
    FROM (
        SELECT
            u.id AS user_id,
            GREATEST(
                (COUNT(DISTINCT l.id) * 3) +
                (COUNT(DISTINCT pv.id) * 1) -
                (COUNT(DISTINCT r.id) * 5),
            0) AS total
        FROM users u
        LEFT JOIN likes l          ON l.liked_id    = u.id
        LEFT JOIN profile_views pv ON pv.viewed_id  = u.id
        LEFT JOIN reports r        ON r.reported_id = u.id
        GROUP BY u.id
    ) s
    WHERE p.user_id = s.user_id;
END;
$$ LANGUAGE plpgsql;
