import os
from pathlib import Path


class DefaultConfig:
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")

    LOGGING_CONFIG = {
        "version": 1,
        "formatters": {
            "default": {"format": "[%(asctime)s] %(levelname)s: %(message)s"},
            "error": {
                "format": "[%(asctime)s] %(levelname)s in %(pathname)s:\n  module:%(module)s\n  line:%(lineno)s\n\
                            message:%(message)s\n"
            },
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            },
            "file": {
                "class": "logging.FileHandler",
                "level": "ERROR",
                "formatter": "error",
                "filename": "logs/errors.log",
            },
        },
        "root": {"level": "INFO", "handlers": ["wsgi", "file"]},
    }


class ProductionConfig(DefaultConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL_PRODUCTION")
    DEBUG = False


class StagingConfig(DefaultConfig):
    DEVELOPMENT = True
    DEBUG = False


class DevelopmentConfig(DefaultConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL_DEVELOPMENT")
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(DefaultConfig):
    TESTING = True
