from flask import Blueprint, jsonify
from app.utils.helpers import token_required

order_bp = Blueprint("orders", __name__)

@order_bp.route("/secure-test", methods=["GET"])
@token_required
def secure_test(user_id, role):
    return jsonify({
        "message": "Protected route accessed successfully",
        "user_id": user_id,
        "role": role
    }), 200