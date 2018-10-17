import os


class BaseConfig:
    DEBOG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG_TB_ENABLED = False              # new
    DEBUG_TB_INTERCEPT_REDIRECTS = False  # new
    BCRYPT_LOG_ROUNDS = 13
    TOKEN_EXPIRATION_DAYS = 30
    TOKEN_EXPIRATION_SECONDS = 0


class DevelopmentConfig(BaseConfig):
    MONGODB_HOST = os.environ.get('DATABASE_URL')
    DEBUG_TB_ENABLED = True  # new
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    TESTING = True
    MONGODB_HOST = os.environ.get('DATABASE_TEST_URL')
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRATION_DAYS = 0
    TOKEN_EXPIRATION_SECONDS = 4


class ProductionConfig(BaseConfig):
    MONGODB_HOST = os.environ.get('DATABASE_URL')
    DEBUG = False


class StagingConfig(BaseConfig):
    MONGODB_HOST = os.environ.get('DATABASE_URL')
