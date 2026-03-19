import psycopg2
from app.config.config import Config

def setup_database():
    """
    This script creates all the tables needed for the restaurant service.
    Run this ONCE before starting the app for the first time.
    """

    conn = psycopg2.connect(Config.DATABASE_URL)
    cursor = conn.cursor()

    # Create the 'users' table
    # IF NOT EXISTS means it won't crash if the table already exists
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id       SERIAL PRIMARY KEY,
        name     VARCHAR(100)  NOT NULL,
        email    VARCHAR(150)  UNIQUE NOT NULL,
        password VARCHAR(255)  NOT NULL,
        phone    VARCHAR(15)   NOT NULL,
        role     VARCHAR(20)   DEFAULT 'customer',
        created_at TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
    );
    """

    cursor.execute(create_users_table)
    conn.commit()

    print("✅ 'users' table created successfully (or already exists).")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    setup_database()
