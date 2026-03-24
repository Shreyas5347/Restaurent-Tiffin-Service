from app.utils.security import verify_password, hash_password, generate_token
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

    user_id = user[0]
    # In table: id (0), name (1), email (2), password (3), phone (4), role (5), created_at (6)
    role = user[5] if len(user) > 5 else "customer"  

    token = generate_token(user_id, role)

    return {
        "message": "Login successful",
        "user_id": user_id,
        "token": token
    }, 200

def admin_login(email, password):
    user = get_user_by_email(email)

    if not user:
        return {"error": "Admin not found"}, 404

    stored_password = user[3]  # password column

    if not verify_password(password, stored_password):
        return {"error": "Invalid password"}, 401

    # In table: id (0), name (1), email (2), password (3), phone (4), role (5), created_at (6)
    role = user[5] if len(user) > 5 else "customer"

    if role != "admin":
        return {"error": "Access denied. Admin role required."}, 403

    user_id = user[0]
    token = generate_token(user_id, role)

    return {
        "message": "Admin Login successful",
        "user_id": user_id,
        "token": token
    }, 200