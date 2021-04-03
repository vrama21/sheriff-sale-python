import os
from .constants import LOG_DIR


class DefaultConfig:
    CSRF_ENABLED = True
    SCHEDULER_API_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False


class ProductionConfig(DefaultConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL_PRODUCTION')


class StagingConfig(DefaultConfig):
    DEBUG = False
    DEVELOPMENT = True


class DevelopmentConfig(DefaultConfig):
    DEVELOPMENT = True
    DEBUG = False
    LOGGING_CONFIG = {
        'version': 1,
        'formatters': {
            'default': {'format': '[%(asctime)s] %(levelname)s: %(message)s'},
            'error': {
                'format': '[%(asctime)s] %(levelname)s in %(pathname)s:\n  module:%(module)s\n  line:%(lineno)s\n\
                                message:%(message)s\n'
            },
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default',
            },
            'file': {
                'class': 'logging.FileHandler',
                'level': 'ERROR',
                'formatter': 'error',
                'filename': str(LOG_DIR / 'errors.log'),
            },
        },
        'root': {'level': 'INFO', 'handlers': ['wsgi', 'file']},
    }
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL_DEVELOPMENT')


class TestingConfig(DefaultConfig):
    TESTING = True
