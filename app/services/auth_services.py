from app.models.user_model import create_user, get_user_by_email
from app.utils.security import hash_password

def register_user(name, email, password, phone):

    # check if user exists
    existing_user = get_user_by_email(email)
    if existing_user:
        return {"error": "User already exists"}, 400

    hashed_password = hash_password(password)

    user_id = create_user(name, email, hashed_password, phone)

    return {
        "message": "User registered successfully",
        "user_id": user_id
    }, 201