import psycopg2
import os
from dotenv import load_dotenv

load_dotenv(override=False)

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", os.getenv("POSTGRES_DB")),
        user=os.getenv("DB_USER", os.getenv("POSTGRES_USER")),
        password=os.getenv("DB_PASSWORD", os.getenv("POSTGRES_PASSWORD")),
        port=int(os.getenv("DB_PORT", 5432))
    )