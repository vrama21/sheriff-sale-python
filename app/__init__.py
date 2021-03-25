import logging
import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .constants import BUILD_DIR, LOG_DIR
from flask_apscheduler import APScheduler


cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
scheduler = APScheduler()


def create_app():
    app = Flask(__name__, static_folder=str(BUILD_DIR), static_url_path='')

    flask_env = os.environ.get('FLASK_ENV')
    if flask_env == 'development':
        load_dev_environment(app)
    elif flask_env == 'production':
        load_prod_environment(app)

    # Initialize Plugins
    db.init_app(app)
    migrate.init_app(app, db)
    scheduler.init_app(app)

    with app.app_context():
        from .commands import cli
        from .routes import routes
        from .tasks import daily_scrape
        scheduler.start()

        if app.config['SQLALCHEMY_DATABASE_URI']:
            db.create_all()

        app.cli.add_command(cli)

        app.register_blueprint(blueprint=routes.main_bp)

        return app


def load_dev_environment(app):
    cors.init_app(app)
    app.config.from_object('app.config.DevelopmentConfig')

    if not LOG_DIR.exists():
        LOG_DIR.mkdir(parents=True, exist_ok=True)

    if not (LOG_DIR / 'errors.log').exists():
        (LOG_DIR / 'errors.log').touch()

    app.logger.setLevel(logging.INFO)


def load_prod_environment(app):
    app.config.from_object('app.config.ProductionConfig')
