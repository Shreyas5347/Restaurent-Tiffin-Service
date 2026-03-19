import psycopg2
from app.config.config import Config

def get_db_connection():
    try:
        conn = psycopg2.connect(Config.DATABASE_URL)
        return conn
    except psycopg2.OperationalError as e:
        raise Exception(f"Could not connect to database. Check your DATABASE_URL in .env\nError: {e}")