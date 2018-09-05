import os


class BaseConfig:
    TESTING = False
    SECRET_KEY = 'my_precious'
    DEBUG_TB_ENABLED = False              # new
    DEBUG_TB_INTERCEPT_REDIRECTS = False  # new


class DevelopmentConfig(BaseConfig):
    MONGODB_HOST = os.environ.get('DATABASE_URL')
    DEBUG_TB_ENABLED = True  # new


class TestingConfig(BaseConfig):
    TESTING = True
    MONGODB_HOST = os.environ.get('DATABASE_TEST_URL')


class ProductionConfig(BaseConfig):
    MONGODB_HOST = os.environ.get('DATABASE_URL')
