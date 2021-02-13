from logging.config import dictConfig
from pathlib import Path
import os
import sys

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from .utils import load_json_data

# For relative imports to work
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

log_path = Path(__file__).parent / 'logs'
if not log_path.exists():
    log_path.mkdir()

logging_config = load_json_data('logging_config.json')
dictConfig(logging_config)

app = Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = os.environ.get('DATABASE_SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main.db"
# app.config.from_object(os.environ.get('APP_SETTINGS'))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from .routes import routes # pylint: disable=wrong-import-position
