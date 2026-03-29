import razorpay
import json
from app.config.config import Config
from app.database.db import get_db_connection
from app.models.payment_model import (
    create_payment, 
    update_payment_with_razorpay, 
    get_payment_by_razorpay_order_id, 
    update_order_status
)
from app.utils.helpers import client as razorpay_client

def create_razorpay_order(user_id, order_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Step 1: Get order
        cursor.execute("SELECT user_id, total_price, status FROM orders WHERE id = %s;", (order_id,))
        order = cursor.fetchone()

        if not order:
            return {"error": "Order not found"}, 404

        db_user_id, total_price, status = order

        # Step 2: Check ownership
        if db_user_id != user_id:
            return {"error": "Unauthorized"}, 403

        # Step 3: Check already paid
        if status == "paid":
            return {"error": "Order already paid"}, 400

    finally:
        cursor.close()
        conn.close()

    # Step 4: Create order in Razorpay
    amount_in_paise = int(float(total_price) * 100)
    data = {
        "amount": amount_in_paise, 
        "currency": "INR", 
        "receipt": str(order_id)
    }
    
    try:
        razorpay_order = razorpay_client.order.create(data=data)
        razorpay_order_id = razorpay_order['id']
    except Exception as e:
        return {"error": f"Failed to create Razorpay order: {str(e)}"}, 500

    # Step 5: Create payment record in pending state
    create_payment(order_id, total_price, status="pending", razorpay_order_id=razorpay_order_id)

    return {
        "message": "Order created successfully",
        "razorpay_order_id": razorpay_order_id,
        "amount": amount_in_paise,
        "currency": "INR",
        "key_id": Config.RAZORPAY_KEY_ID
    }, 200

def handle_razorpay_webhook(payload_body, signature_header):
    try:
        # Verify webhook signature using the raw payload body and signature header.
        # Ensure RAZORPAY_WEBHOOK_SECRET is correctly set in environment.
        if not Config.RAZORPAY_WEBHOOK_SECRET:
            return {"error": "Webhook secret not configured"}, 500

        payload_str = payload_body.decode("utf-8") if isinstance(payload_body, bytes) else payload_body
        razorpay_client.utility.verify_webhook_signature(
            payload_str,
            signature_header, 
            Config.RAZORPAY_WEBHOOK_SECRET
        )
    except razorpay.errors.SignatureVerificationError:
        return {"error": "Invalid signature"}, 400
    except Exception as e:
        return {"error": str(e)}, 400

    # Parse payload
    try:
        data = json.loads(payload_body)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON payload"}, 400

    event_type = data.get('event')

    # Handle payment authorized or captured
    if event_type in ['payment.captured', 'order.paid']:
        payment_entity = data['payload']['payment']['entity']
        razorpay_order_id = payment_entity.get('order_id')
        razorpay_payment_id = payment_entity.get('id')
        payment_method = payment_entity.get('method')
        
        # Find the payment record
        payment_record = get_payment_by_razorpay_order_id(razorpay_order_id)
        if not payment_record:
            return {"error": "Payment record not found"}, 404
            
        if payment_record['status'] == 'success':
            # Idempotency check: Already processed
            return {"message": "Already processed"}, 200

        # Update payment and order records
        update_payment_with_razorpay(
            razorpay_order_id=razorpay_order_id, 
            status="success", 
            razorpay_payment_id=razorpay_payment_id, 
            payment_method=payment_method
        )
        update_order_status(payment_record['order_id'], "paid")

    elif event_type == 'payment.failed':
        payment_entity = data['payload']['payment']['entity']
        razorpay_order_id = payment_entity.get('order_id')
        
        payment_record = get_payment_by_razorpay_order_id(razorpay_order_id)
        if payment_record and payment_record['status'] == 'pending':
            update_payment_with_razorpay(
                razorpay_order_id=razorpay_order_id, 
                status="failed"
            )

    return {"message": "Webhook processed successfully"}, 200