import os


class BaseConfig:
    TESTING = False


class DevelopmentConfig(BaseConfig):
    MONGODB_HOST = os.environ.get('DATABASE_URL')


class TestingConfig(BaseConfig):
    TESTING = True
    MONGODB_HOST = os.environ.get('DATABASE_TEST_URL')


class ProductionConfig(BaseConfig):
    MONGODB_HOST = os.environ.get('DATABASE_URL')
