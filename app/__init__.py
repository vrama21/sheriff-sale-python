import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from .constants import ROOT_DIR, BUILD_DIR, STATIC_DIR

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__, static_folder=str(BUILD_DIR), static_url_path='/')

    # for k, v in app.config.items():
    #     print(k, v)

    flask_env = os.environ.get('FLASK_ENV')
    if flask_env == 'development':
        app.config.from_object('app.config.DevelopmentConfig')
    elif flask_env == 'production':
        app.config.from_object('app.config.ProductionConfig')

    # Initialize Plugins
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

        from .commands import cli
        from .routes import routes

        app.cli.add_command(cli)

        app.register_blueprint(
            blueprint=routes.main_bp,
            static_folder=str(STATIC_DIR),
            static_url_path='/static',
        )

        return app
