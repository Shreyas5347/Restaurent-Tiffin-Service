from flask import Flask
from app.config.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register routes
    from app.routes.auth_routes import auth_bp
    from app.routes.menu_routes import menu_bp
    from app.routes.order_routes import order_bp
    from app.routes.payment_routes import payment_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(menu_bp, url_prefix="/menu")
    app.register_blueprint(order_bp, url_prefix="/orders")
    app.register_blueprint(payment_bp, url_prefix="/payments")

@app.route("/")
def index():
    return "Restaurant Service API is running!"


    return app