import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '17a202d87bb99ee84fd5ebbec5130e0f'
    SQLALCHEMY_DATABASE_URI = 'postgresql:///main'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
