from app.database.db import get_db_connection


def get_all_categories():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, key, name, icon FROM categories ORDER BY id;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [
        {"id": row[0], "key": row[1], "name": row[2], "icon": row[3]}
        for row in rows
    ]


def add_category(key, name, icon="🍽️"):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO categories (key, name, icon)
    VALUES (%s, %s, %s)
    RETURNING id;
    """
    cursor.execute(query, (key, name, icon))
    cat_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return cat_id


def update_category(cat_id, key, name, icon):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    UPDATE categories
    SET key = %s, name = %s, icon = %s
    WHERE id = %s
    RETURNING id;
    """
    cursor.execute(query, (key, name, icon, cat_id))
    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return result[0] if result else None


def delete_category(cat_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE id = %s RETURNING id;", (cat_id,))
    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return result[0] if result else None
