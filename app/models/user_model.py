from app.database.db import get_db_connection

def create_user(name, email, password, phone):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO users (name, email, password, phone)
    VALUES (%s, %s, %s, %s)
    RETURNING id;
    """

    cursor.execute(query, (name, email, password, phone))
    user_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return user_id


def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE email = %s;"
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user