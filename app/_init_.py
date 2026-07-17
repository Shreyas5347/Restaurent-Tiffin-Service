from flask import Flask
from flask_cors import CORS
from app.config.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Read allowed origins from env variable (supports comma-separated list)
    origins = [o.strip() for o in Config.CORS_ORIGINS.split(",")]
    CORS(app, resources={r"/*": {"origins": origins}}, supports_credentials=True)

    # Register routes
    from app.routes.auth_routes import auth_bp
    from app.routes.menu_routes import menu_bp
    from app.routes.order_routes import order_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(menu_bp, url_prefix="/menu")
    app.register_blueprint(order_bp, url_prefix="/orders")

    @app.route("/")
    def index():
        return "Restaurant Service API is running!"


    return app