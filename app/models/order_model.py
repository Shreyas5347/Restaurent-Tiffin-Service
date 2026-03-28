from app.database.db import get_db_connection


def place_order(user_id, items):
    """
    Place a new order for a user.
    `items` is a list of dicts: [{"menu_item_id": 1, "quantity": 2}, ...]
    Returns the new order_id and total_price.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Fetch price for each menu item to create a price snapshot
        total_price = 0.0
        enriched_items = []

        for item in items:
            cursor.execute(
                "SELECT id, price FROM menu_items WHERE id = %s;",
                (item["menu_item_id"],)
            )
            menu_item = cursor.fetchone()
            if not menu_item:
                raise ValueError(f"Menu item with id {item['menu_item_id']} not found.")

            unit_price = float(menu_item[1])
            quantity = item["quantity"]
            total_price += unit_price * quantity
            enriched_items.append({
                "menu_item_id": menu_item[0],
                "quantity": quantity,
                "unit_price": unit_price
            })

        # Insert into orders table
        cursor.execute(
            """
            INSERT INTO orders (user_id, status, total_price)
            VALUES (%s, 'pending', %s)
            RETURNING id;
            """,
            (user_id, total_price)
        )
        order_id = cursor.fetchone()[0]

        # Insert each item into order_items
        for item in enriched_items:
            cursor.execute(
                """
                INSERT INTO order_items (order_id, menu_item_id, quantity, unit_price)
                VALUES (%s, %s, %s, %s);
                """,
                (order_id, item["menu_item_id"], item["quantity"], item["unit_price"])
            )

        conn.commit()
        return {"order_id": order_id, "total_price": round(total_price, 2)}

    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def get_order_by_id(order_id):
    """Fetch a single order with all its items."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT o.id, o.user_id, o.status, o.total_price, o.created_at
        FROM orders o
        WHERE o.id = %s;
        """,
        (order_id,)
    )
    row = cursor.fetchone()

    if not row:
        cursor.close()
        conn.close()
        return None

    order = {
        "id": row[0],
        "user_id": row[1],
        "status": row[2],
        "total_price": float(row[3]),
        "created_at": str(row[4]),
        "items": []
    }

    cursor.execute(
        """
        SELECT oi.id, oi.menu_item_id, m.name, oi.quantity, oi.unit_price
        FROM order_items oi
        JOIN menu_items m ON oi.menu_item_id = m.id
        WHERE oi.order_id = %s;
        """,
        (order_id,)
    )
    for item_row in cursor.fetchall():
        order["items"].append({
            "order_item_id": item_row[0],
            "menu_item_id": item_row[1],
            "name": item_row[2],
            "quantity": item_row[3],
            "unit_price": float(item_row[4])
        })

    cursor.close()
    conn.close()
    return order


def get_orders_by_user(user_id):
    """Fetch all orders placed by a specific customer."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, status, total_price, created_at
        FROM orders
        WHERE user_id = %s
        ORDER BY created_at DESC;
        """,
        (user_id,)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return [
        {
            "id": row[0],
            "status": row[1],
            "total_price": float(row[2]),
            "created_at": str(row[3])
        }
        for row in rows
    ]


def get_all_orders():
    """Admin: fetch every order from all users."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT o.id, o.user_id, u.name, o.status, o.total_price, o.created_at
        FROM orders o
        JOIN users u ON o.user_id = u.id
        ORDER BY o.created_at DESC;
        """
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return [
        {
            "id": row[0],
            "user_id": row[1],
            "customer_name": row[2],
            "status": row[3],
            "total_price": float(row[4]),
            "created_at": str(row[5])
        }
        for row in rows
    ]


def update_order_status(order_id, new_status):
    """Admin: update the status of an order."""
    VALID_STATUSES = {"pending", "confirmed", "preparing", "delivered", "cancelled"}
    if new_status not in VALID_STATUSES:
        raise ValueError(f"Invalid status '{new_status}'. Must be one of: {', '.join(VALID_STATUSES)}")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE orders
        SET status = %s
        WHERE id = %s
        RETURNING id;
        """,
        (new_status, order_id)
    )
    updated = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    return updated[0] if updated else None
