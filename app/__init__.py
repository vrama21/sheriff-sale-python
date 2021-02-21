from pathlib import Path

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.DevelopmentConfig')
    CORS(app)

    # Create log directory if it doesn't exist
    log_path = Path(__file__).parent.parent / 'logs'
    if not log_path.exists():
        log_path.mkdir()

    # Initialize Plugins
    db.init_app(app)
    migrate.init_app(app)

    with app.app_context():
        from .commands import create_tables, drop_tables
        from .routes import routes

        app.cli.add_command(create_tables)
        app.cli.add_command(drop_tables)

        db.create_all()

        app.register_blueprint(routes.main_bp)

        return app