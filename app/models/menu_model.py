from app.database.db import get_db_connection

def add_menu_item(name, description, price, category="Uncategorized"):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO menu_items (name, description, price, category)
    VALUES (%s, %s, %s, %s)
    RETURNING id;
    """

    cursor.execute(query, (name, description, price, category))
    item_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return item_id

def get_all_menu_items():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT id, name, description, price, category, created_at FROM menu_items;"
    cursor.execute(query)
    
    # fetchall returns a list of tuples
    items = cursor.fetchall()

    cursor.close()
    conn.close()

    # Format into a list of dictionaries for easier JSON response
    return [
        {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "price": float(row[3]),
            "category": row[4],
            "created_at": row[5]
        }
        for row in items
    ]

def update_menu_item(item_id, name, description, price, category):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE menu_items
    SET name = %s, description = %s, price = %s, category = %s
    WHERE id = %s
    RETURNING id;
    """

    cursor.execute(query, (name, description, price, category, item_id))
    updated_id = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    return updated_id[0] if updated_id else None

def delete_menu_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM menu_items WHERE id = %s RETURNING id;"

    cursor.execute(query, (item_id,))
    deleted_id = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    return deleted_id[0] if deleted_id else None
