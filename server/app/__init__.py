import os
from pathlib import Path
import sys

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .commands import create_tables, drop_tables

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.configs.config.DevelopmentConfig')
    CORS(app)

    # Create log directory if it doesn't exist
    log_path = Path(__file__).parent.parent / 'logs'
    if not log_path.exists():
        log_path.mkdir()

    # Initialize Plugins
    db.init_app(app)
    migrate.init_app(app)

    with app.app_context():
        from .routes import routes

        app.cli.add_command(create_tables)
        app.cli.add_command(drop_tables)

        app.register_blueprint(routes.main_bp)

        return app
