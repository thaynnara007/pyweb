import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object): 
    TESTING = False
    CSRF_ENABLED = True
    POSTS_PER_PAGE = 25
    SECRET_KEY = os.environ.get("SECRET_KEY") or "The eleventh metal"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "postgresql:///SwaBook"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


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
