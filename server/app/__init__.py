from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_graphql import GraphQLView
from logging.config import dictConfig
from .utils import load_json_data
from pathlib import Path

log_path = Path(__file__).parent / 'logs'
if not log_path.exists():
    log_path.mkdir()

logging_config = load_json_data('logging_config.json')
dictConfig(logging_config)

app = Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = "17a202d87bb99ee84fd5ebbec5130e0f"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgressql:///main.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from . import routes
