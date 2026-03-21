from app.utils.security import verify_password, hash_password
from app.models.user_model import get_user_by_email, create_user

def register_user(name, email, password, phone):
    existing_user = get_user_by_email(email)
    if existing_user:
        return {"error": "Email already registered"}, 400
    
    hashed_password = hash_password(password)
    user_id = create_user(name, email, hashed_password, phone)
    return {"message": "User registered successfully", "user_id": user_id}, 201

def login_user(email, password):

    user = get_user_by_email(email)

    if not user:
        return {"error": "User not found"}, 404

    stored_password = user[3]  # password column

    if not verify_password(password, stored_password):
        return {"error": "Invalid password"}, 401

    return {
        "message": "Login successful",
        "user_id": user[0]
    }, 200