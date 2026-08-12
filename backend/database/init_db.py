import logging
import os
import time

from database.db import get_connection

logger = logging.getLogger(__name__)

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")
SCHEMA_APPLY_RETRIES = 5
SCHEMA_APPLY_RETRY_DELAY_S = 2


def apply_schema():
    """Applies schema.sql at startup (idempotent: CREATE IF NOT EXISTS everywhere).
    Retries a few times while the DB becomes ready."""
    for attempt in range(SCHEMA_APPLY_RETRIES):
        try:
            run_schema_file()
            return
        except Exception:
            if attempt == SCHEMA_APPLY_RETRIES - 1:
                logger.exception("Schema could not be applied after %s attempts", SCHEMA_APPLY_RETRIES)
                return
            logger.info("Database not ready, retrying schema apply (%s/%s)", attempt + 1, SCHEMA_APPLY_RETRIES)
            time.sleep(SCHEMA_APPLY_RETRY_DELAY_S)


def run_schema_file():
    """Runs the contents of schema.sql against the DB."""
    with open(SCHEMA_PATH) as schema_file:
        schema_sql = schema_file.read()

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(schema_sql)
        conn.commit()
        cur.close()
    finally:
        conn.close()
