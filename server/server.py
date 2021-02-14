import json
from logging.config import dictConfig
from pathlib import Path
import os
import sys

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


def create_app():
    from .app import routes  # pylint: disable=import-outside-toplevel

    # For relative imports to work
    sys.path.append(os.path.dirname(os.path.realpath(__file__)))

    # Create log directory if it doesn't exist
    log_path = Path(__file__).parent / 'logs'
    if not log_path.exists():
        log_path.mkdir()

    # Setup logging configuration
    logging_config = None
    with open('logging_config.json', 'r') as file:
        logging_config = json.loads(file)
    dictConfig(logging_config)

    app = Flask(__name__)
    CORS(app)

    app.config.from_object(os.environ.get('APP_SETTINGS'))
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db = SQLAlchemy(app)
