import logging
import os

import flask_migrate
from flask import Flask
from flask_apscheduler import APScheduler
from flask_cors import CORS
from flask_googlemaps import GoogleMaps
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from app.constants import BUILD_DIR, LOG_DIR, MIGRATIONS_DIR

cors = CORS()
db = SQLAlchemy()
migrate = flask_migrate.Migrate()
scheduler = APScheduler()
google_maps = GoogleMaps()
jwt = JWTManager()


def create_app():
    app = Flask(__name__, static_folder=str(BUILD_DIR), static_url_path='')

    flask_env = os.environ.get('FLASK_ENV')
    if flask_env == 'development':
        load_dev_environment(app)
    elif flask_env == 'production':
        load_prod_environment(app)

    # Initialize Plugins
    db.init_app(app)
    google_maps.init_app(app)
    migrate.init_app(app, db, directory=str(MIGRATIONS_DIR))
    scheduler.init_app(app)

    with app.app_context():
        from .commands import cli
        from .routes import main_bp

        db.create_all()
        flask_migrate.upgrade()

        app.cli.add_command(cli)

        app.register_blueprint(blueprint=main_bp)

        scheduler.start()

        return app


def load_dev_environment(app):
    CORS(app)
    app.config.from_object('app.config.DevelopmentConfig')

    if not LOG_DIR.exists():
        LOG_DIR.mkdir(parents=True, exist_ok=True)

    if not (LOG_DIR / 'errors.log').exists():
        (LOG_DIR / 'errors.log').touch()

    app.logger.setLevel(logging.INFO)


def load_prod_environment(app):
    app.config.from_object('app.config.ProductionConfig')
