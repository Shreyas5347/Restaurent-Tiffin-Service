from app.database.db import get_db_connection

def create_payment(order_id, amount, status="pending", razorpay_order_id=None):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        try:
            query = """
            INSERT INTO payments (order_id, amount, status, razorpay_order_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
            """
            cursor.execute(query, (order_id, amount, status, razorpay_order_id))
            payment_id = cursor.fetchone()[0]
            conn.commit()
            return payment_id
        finally:
            cursor.close()
    finally:
        conn.close()

def update_payment_with_razorpay(razorpay_order_id, status, razorpay_payment_id=None, razorpay_signature=None, payment_method=None):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        try:
            query = """
            UPDATE payments 
            SET status = %s, razorpay_payment_id = %s, razorpay_signature = %s, payment_method = %s
            WHERE razorpay_order_id = %s;
            """
            cursor.execute(query, (status, razorpay_payment_id, razorpay_signature, payment_method, razorpay_order_id))
            conn.commit()
        finally:
            cursor.close()
    finally:
        conn.close()

def get_payment_by_razorpay_order_id(razorpay_order_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        try:
            query = "SELECT id, order_id, amount, status FROM payments WHERE razorpay_order_id = %s;"
            cursor.execute(query, (razorpay_order_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "order_id": row[1],
                    "amount": float(row[2]),
                    "status": row[3]
                }
            return None
        finally:
            cursor.close()
    finally:
        conn.close()

def update_order_status(order_id, status):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        try:
            query = "UPDATE orders SET status = %s WHERE id = %s;"
            cursor.execute(query, (status, order_id))
            conn.commit()
        finally:
            cursor.close()
    finally:
        conn.close()