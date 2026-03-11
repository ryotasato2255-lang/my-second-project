from pathlib import Path
from flask import Flask
from .config import Config
from .routes import main_bp

ROOT = Path(__file__).parent.parent


def create_app(config_class=Config):
    app = Flask(
        __name__,
        template_folder=str(ROOT / "templates"),
    )
    app.config.from_object(config_class)
    app.register_blueprint(main_bp)
    return app
