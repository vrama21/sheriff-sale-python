import os
from pathlib import Path
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import registry
from .constants import BUILD_DIR

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__, static_folder=str(BUILD_DIR), static_url_path='')

    flask_env = os.environ.get('FLASK_ENV')
    if flask_env == 'development':
        app.config.from_object('app.config.DevelopmentConfig')
        cors.init_app(app)
    elif flask_env == 'production':
        app.config.from_object('app.config.ProductionConfig')

    # Initialize Plugins
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from .commands import cli
        from .routes import routes

        if app.config['SQLALCHEMY_DATABASE_URI']:
            db.create_all()

        app.cli.add_command(cli)

        app.register_blueprint(blueprint=routes.main_bp)

        return app
