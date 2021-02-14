from pathlib import Path


class DefaultConfig:
    basedir = Path(__file__).resolve().parent.parent

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "17a202d87bb99ee84fd5ebbec5130e0f"
    SQLALCHEMY_DATABASE_URI = "postgresql:///main"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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
                "filename": Path(basedir / 'logs' / 'errors.log'),
            },
        },
        "root": {"level": "INFO", "handlers": ["wsgi", "file"]},
    }


class ProductionConfig(DefaultConfig):
    DEBUG = False


class StagingConfig(DefaultConfig):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(DefaultConfig):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(DefaultConfig):
    TESTING = True
