import os
import time

from database.db import get_connection

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")
SCHEMA_APPLY_RETRIES = 5
SCHEMA_APPLY_RETRY_DELAY_S = 2


def apply_schema():
    """Applique schema.sql au démarrage (idempotent : CREATE IF NOT EXISTS partout).
    Réessaie quelques fois le temps que la DB soit prête."""
    for attempt in range(SCHEMA_APPLY_RETRIES):
        try:
            run_schema_file()
            return
        except Exception as error:
            if attempt == SCHEMA_APPLY_RETRIES - 1:
                print(f"init_db: schema non appliqué ({error})")
                return
            time.sleep(SCHEMA_APPLY_RETRY_DELAY_S)


def run_schema_file():
    """Exécute le contenu de schema.sql sur la DB."""
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
