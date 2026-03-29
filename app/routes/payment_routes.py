from flask import Blueprint, request, jsonify
from app.services.payment_service import create_razorpay_order, handle_razorpay_webhook
from app.utils.helpers import token_required

payment_bp = Blueprint("payments", __name__)

@payment_bp.route("/create-order", methods=["POST"])
@token_required
def create_order(user_id, role):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be provided"}), 400

    order_id = data.get("order_id")

    if not order_id:
        return jsonify({"error": "order_id is required"}), 400

    response, status = create_razorpay_order(user_id, order_id)

    return jsonify(response), status

@payment_bp.route("/webhook", methods=["POST"])
def webhook():
    # Razorpay webhook sends the raw body and X-Razorpay-Signature in headers
    payload_body = request.get_data()
    signature_header = request.headers.get("X-Razorpay-Signature")

    if not signature_header:
        return jsonify({"error": "Missing signature header"}), 400

    response, status = handle_razorpay_webhook(payload_body, signature_header)

    return jsonify(response), status