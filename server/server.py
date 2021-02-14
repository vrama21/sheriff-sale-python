import os
from pathlib import Path
import sys

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
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

# Set up Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models import *
from app.routes import routes  # noqa: E402

db.create_all()