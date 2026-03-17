from app.database.db import get_db_connection

def test_connection():
    try:
        conn = get_db_connection()
        print("✅ Successfully connected to the PostgreSQL database!")
        
        # Optionally, get the PostgreSQL version to confirm it works
        cur = conn.cursor()
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(f"📦 PostgreSQL version: {db_version[0]}")
        
        cur.close()
        conn.close()
        print("Connection closed.")
    except Exception as e:
        print(f"❌ Failed to connect to the database.\nError: {e}")

if __name__ == "__main__":
    test_connection()
