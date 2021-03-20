import os
from pathlib import Path
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from whitenoise import WhiteNoise

ROOT_DIR = Path(__file__).parent
BUILD_DIR = ROOT_DIR / 'build'
STATIC_DIR = BUILD_DIR / '/static'

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__, static_folder=str(BUILD_DIR), static_url_path='/')

    for k, v in app.config.items():
        print(k, v)
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
        from .commands import cli
        from .routes import routes

        db.create_all()

        app.cli.add_command(cli)

        app.register_blueprint(
            blueprint=routes.main_bp,
            static_folder=STATIC_DIR,
            static_url_path='/home-static',
        )

        # app.wsgi_app = WhiteNoise(app.wsgi_app, root=BUILD_DIR)

        return app
