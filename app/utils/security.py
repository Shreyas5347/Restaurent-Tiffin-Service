import jwt
import datetime
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    return generate_password_hash(password)

def verify_password(password, hashed_password):
    return check_password_hash(hashed_password, password)

def generate_token(user_id, role="customer"):
    """Generate a signed JWT token valid for 1 day."""
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        "iat": datetime.datetime.utcnow()
    }
    secret = current_app.config["JWT_SECRET_KEY"]
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token

def decode_token(token):
    """Decode and validate a JWT token. Returns the payload dict."""
    secret = current_app.config["JWT_SECRET_KEY"]
    # jwt.decode raises exceptions on invalid/expired tokens
    payload = jwt.decode(token, secret, algorithms=["HS256"])
    return payload