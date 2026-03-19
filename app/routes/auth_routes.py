from flask import request, Blueprint, jsonify
from app.services.auth_services import register_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # Make sure the request body actually has data
    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")

    # Check that all required fields are present
    if not all([name, email, password, phone]):
        return jsonify({"error": "name, email, password, and phone are all required"}), 400

    response, status = register_user(name, email, password, phone)
    return jsonify(response), status