from flask import Blueprint, request, jsonify
from app.utils.helpers import token_required, admin_required
from app.models.order_model import (
    place_order,
    get_order_by_id,
    get_orders_by_user,
    get_all_orders,
    update_order_status
)

order_bp = Blueprint("orders", __name__)


# ──────────────────────────────────────────────
#  CUSTOMER ROUTES
# ──────────────────────────────────────────────

@order_bp.route("/", methods=["POST"])
@token_required
def place_order_route(user_id, role):
    """
    Customer places a new order.
    Body: { "items": [{"menu_item_id": 1, "quantity": 2}, ...] }
    """
    data = request.get_json()

    if not data or "items" not in data:
        return jsonify({"error": "Request body must include 'items' list"}), 400

    items = data["items"]

    if not isinstance(items, list) or len(items) == 0:
        return jsonify({"error": "'items' must be a non-empty list"}), 400

    for item in items:
        if "menu_item_id" not in item or "quantity" not in item:
            return jsonify({"error": "Each item must have 'menu_item_id' and 'quantity'"}), 400
        if not isinstance(item["quantity"], int) or item["quantity"] < 1:
            return jsonify({"error": "Quantity must be a positive integer"}), 400

    try:
        result = place_order(user_id, items)
        return jsonify({
            "message": "Order placed successfully",
            "order_id": result["order_id"],
            "total_price": result["total_price"]
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@order_bp.route("/my", methods=["GET"])
@token_required
def my_orders(user_id, role):
    """
    Customer views their own order history.
    """
    try:
        orders = get_orders_by_user(user_id)
        return jsonify(orders), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@order_bp.route("/<int:order_id>", methods=["GET"])
@token_required
def get_order(user_id, role, order_id):
    """
    View a specific order by ID.
    Customers can only view their own orders; admins can view any.
    """
    try:
        order = get_order_by_id(order_id)
        if not order:
            return jsonify({"error": "Order not found"}), 404

        # Non-admins can only access their own orders
        if role != "admin" and order["user_id"] != user_id:
            return jsonify({"error": "Access denied"}), 403

        return jsonify(order), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ──────────────────────────────────────────────
#  ADMIN ROUTES
# ──────────────────────────────────────────────

@order_bp.route("/", methods=["GET"])
@admin_required
def list_all_orders(user_id, role):
    """
    Admin: view all orders from all customers.
    """
    try:
        orders = get_all_orders()
        return jsonify(orders), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@order_bp.route("/<int:order_id>/status", methods=["PUT"])
@admin_required
def update_status(user_id, role, order_id):
    """
    Admin: update the status of an order.
    Body: { "status": "confirmed" }
    Valid statuses: pending | confirmed | preparing | delivered | cancelled
    """
    data = request.get_json()

    if not data or "status" not in data:
        return jsonify({"error": "Request body must include 'status'"}), 400

    new_status = data["status"].strip().lower()

    try:
        updated_id = update_order_status(order_id, new_status)
        if updated_id:
            return jsonify({
                "message": f"Order #{updated_id} status updated to '{new_status}'"
            }), 200
        else:
            return jsonify({"error": "Order not found"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500