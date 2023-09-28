import os
from utils import get_full_path


class Config(object):
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOADS_DIR = get_full_path(BASE_DIR, "uploads")


class DevelopmentConfig(Config):
    DEBUG = True
    # other development-specific configurations


class TestingConfig(Config):
    TESTING = True
    # other testing-specific configurations


class ProductionConfig(Config):
    DEBUG = False
    # other production-specific configurations
