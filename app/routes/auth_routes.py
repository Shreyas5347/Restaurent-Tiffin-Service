from flask import request, Blueprint, jsonify
from app.services.auth_services import admin_login
from app.services.auth_services import register_user, login_user

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


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    response, status = login_user(email, password)
    return jsonify(response), status

@auth_bp.route("/admin-login", methods=["POST"])
def admin_login_route():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    
    response, status = admin_login(email, password)
    return jsonify(response), status
