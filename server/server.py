import json
from logging.config import dictConfig
from pathlib import Path
import os
import sys

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

 # For relative imports to work
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# Create log directory if it doesn't exist
log_path = Path(__file__).parent / "logs"
if not log_path.exists():
    log_path.mkdir()

app = Flask(__name__)
CORS(app)

app.config.from_object("app.configs.default.DevelopmentConfig")

db = SQLAlchemy(app)

from app.routes import routes
