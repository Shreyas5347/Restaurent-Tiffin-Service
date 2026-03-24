from flask import Blueprint, request, jsonify
from app.utils.helpers import admin_required
from app.models.menu_model import add_menu_item, get_all_menu_items

menu_bp = Blueprint("menu", __name__)

@menu_bp.route("/items", methods=["POST"])
@admin_required
def create_menu_item(user_id, role):
    """
    Admin-only route to add a new item to the menu.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get("name")
    description = data.get("description", "")
    price = data.get("price")

    if not name or price is None:
        return jsonify({"error": "Name and price are required"}), 400

    try:
        item_id = add_menu_item(name, description, price)
        return jsonify({
            "message": "Menu item added successfully",
            "item_id": item_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@menu_bp.route("/items", methods=["GET"])
def list_menu_items():
    """
    Public route to view the menu.
    """
    try:
        items = get_all_menu_items()
        return jsonify(items), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500