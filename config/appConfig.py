import os

basedir = os.path.abspath(os.path.dirname(__file__))


class AppConfig:
    SECRET_KEY = "b0ef2c932169471ab0e1c2bd1c7d9b07"

    @staticmethod
    def init_app(app):
        pass


class DevelopConfig(AppConfig):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = "mysql://parkinguser:xmrbi404@172.16.52.35/parking2.0_new"
    # os.environ.get("dev.database.url")


class TestConfig(AppConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("test.database.url")


class ProdConfig(AppConfig):
    PROD = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("prod.database.url")


config = {
    "develop": DevelopConfig,
    "test": TestConfig,
    "prod": ProdConfig,
    "default": DevelopConfig,
}
