from flask import Blueprint, request, jsonify
from app.utils.helpers import admin_required
from app.models.settings_model import get_shop_status, set_shop_mode

settings_bp = Blueprint("settings", __name__)


@settings_bp.route("/status", methods=["GET"])
def get_status_route():
    """
    Public route to get current shop status and timings.
    """
    try:
        status_data = get_shop_status()
        return jsonify(status_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@settings_bp.route("/status", methods=["PUT"])
@admin_required
def update_status_route(user_id, role):
    """
    Admin-only route to set shop mode: 'auto' | 'open' | 'closed'.
    Body: { "mode": "open" }
    """
    data = request.get_json()
    if not data or "mode" not in data:
        return jsonify({"error": "Request body must include 'mode' ('auto', 'open', or 'closed')"}), 400

    new_mode = str(data["mode"]).strip().lower()
    try:
        updated_mode = set_shop_mode(new_mode)
        current_status = get_shop_status()
        return jsonify({
            "message": f"Shop mode updated to '{updated_mode}'",
            "status": current_status
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
