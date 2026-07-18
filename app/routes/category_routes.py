from flask import Blueprint, request, jsonify
from app.utils.helpers import admin_required
from app.models.category_model import (
    get_all_categories,
    add_category,
    update_category,
    delete_category,
)

category_bp = Blueprint("categories", __name__)


@category_bp.route("/", methods=["GET"])
def list_categories():
    """Public route — list all categories."""
    try:
        cats = get_all_categories()
        return jsonify(cats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@category_bp.route("/", methods=["POST"])
@admin_required
def create_category(user_id, role):
    """Admin-only — add a new category."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    key  = data.get("key", "").strip().lower()
    name = data.get("name", "").strip()
    icon = data.get("icon", "🍽️").strip()

    if not key or not name:
        return jsonify({"error": "key and name are required"}), 400

    try:
        cat_id = add_category(key, name, icon)
        return jsonify({"message": "Category created", "id": cat_id}), 201
    except Exception as e:
        # Duplicate key violation
        if "unique" in str(e).lower() or "duplicate" in str(e).lower():
            return jsonify({"error": f"A category with key '{key}' already exists"}), 409
        return jsonify({"error": str(e)}), 500


@category_bp.route("/<int:cat_id>", methods=["PUT"])
@admin_required
def edit_category(user_id, role, cat_id):
    """Admin-only — update an existing category."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    key  = data.get("key", "").strip().lower()
    name = data.get("name", "").strip()
    icon = data.get("icon", "🍽️").strip()

    if not key or not name:
        return jsonify({"error": "key and name are required"}), 400

    try:
        updated_id = update_category(cat_id, key, name, icon)
        if updated_id:
            return jsonify({"message": "Category updated", "id": updated_id}), 200
        return jsonify({"error": "Category not found"}), 404
    except Exception as e:
        if "unique" in str(e).lower() or "duplicate" in str(e).lower():
            return jsonify({"error": f"A category with key '{key}' already exists"}), 409
        return jsonify({"error": str(e)}), 500


@category_bp.route("/<int:cat_id>", methods=["DELETE"])
@admin_required
def remove_category(user_id, role, cat_id):
    """Admin-only — delete a category."""
    try:
        deleted_id = delete_category(cat_id)
        if deleted_id:
            return jsonify({"message": "Category deleted", "id": deleted_id}), 200
        return jsonify({"error": "Category not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
