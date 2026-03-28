from flask import Blueprint, request, jsonify
from app.utils.helpers import admin_required
from app.models.menu_model import add_menu_item, get_all_menu_items, update_menu_item, delete_menu_item

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
    category = data.get("category", "Uncategorized")

    if not name or price is None:
        return jsonify({"error": "Name and price are required"}), 400

    try:
        item_id = add_menu_item(name, description, price, category)
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

@menu_bp.route("/items/<int:item_id>", methods=["PUT"])
@admin_required
def update_menu_item_route(user_id, role, item_id):
    """
    Admin-only route to update an existing menu item.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get("name")
    description = data.get("description", "")
    price = data.get("price")
    category = data.get("category", "Uncategorized")

    if not name or price is None:
        return jsonify({"error": "Name and price are required"}), 400

    try:
        updated_id = update_menu_item(item_id, name, description, price, category)
        if updated_id:
            return jsonify({
                "message": "Menu item updated successfully",
                "item_id": updated_id
            }), 200
        else:
            return jsonify({"error": "Menu item not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@menu_bp.route("/items/<int:item_id>", methods=["DELETE"])
@admin_required
def delete_menu_item_route(user_id, role, item_id):
    """
    Admin-only route to delete an existing menu item.
    """
    try:
        deleted_id = delete_menu_item(item_id)
        if deleted_id:
            return jsonify({
                "message": "Menu item deleted successfully",
                "item_id": deleted_id
            }), 200
        else:
            return jsonify({"error": "Menu item not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500