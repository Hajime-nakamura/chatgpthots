from flask import Flask
from flask_cors import CORS
from .config import Config
from .utils.logger import configure_logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, supports_credentials=True,
         resources={r"/v1/*": {"origins": app.config["CORS_ALLOW_ORIGINS"]}})

    configure_logging(app.config.get("LOG_LEVEL", "INFO"))

    from .routes import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/")

    return app
