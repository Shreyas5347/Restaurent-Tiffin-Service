from functools import wraps
from flask import request, jsonify
from app.utils.security import decode_token
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", None)

        if not auth_header:
            return jsonify({"error": "Token is missing"}), 401

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"error": "Invalid Authorization header format. Use: Bearer <token>"}), 401

        token = parts[1]

        try:
            payload = decode_token(token)
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired. Please log in again."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token. Please log in again."}), 401

        return f(user_id=payload["user_id"], role=payload.get("role", "customer"), *args, **kwargs)

    return decorated

def admin_required(f):
   
    @wraps(f)
    @token_required
    def decorated(user_id, role, *args, **kwargs):
        if role != "admin":
            return jsonify({"error": "Access denied. Admin privileges required."}), 403
        return f(user_id=user_id, role=role, *args, **kwargs)
    
    return decorated

