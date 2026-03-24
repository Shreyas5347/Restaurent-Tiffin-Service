from app.database.db import get_db_connection

def add_menu_item(name, description, price):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO menu_items (name, description, price)
    VALUES (%s, %s, %s)
    RETURNING id;
    """

    cursor.execute(query, (name, description, price))
    item_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return item_id

def get_all_menu_items():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT id, name, description, price, created_at FROM menu_items;"
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
            "created_at": row[4]
        }
        for row in items
    ]
