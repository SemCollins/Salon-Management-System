from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
from config import Config
import logging

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    CORS(app)

    # Register only the blueprints that exist in this workspace.
    try:
        from app.main import bp as main_bp
        app.register_blueprint(main_bp)
    except Exception:
        app.logger.warning("main blueprint not found or failed to register.")

    try:
        from app.admin import bp as admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')
    except Exception:
        app.logger.warning("admin blueprint not found or failed to register.")

    # Optional: register auth/api if you later add them
    # try:
    #     from app.auth import bp as auth_bp
    #     app.register_blueprint(auth_bp)
    # except Exception:
    #     pass

    # Basic logging
    logging.basicConfig(level=logging.INFO)

    return app