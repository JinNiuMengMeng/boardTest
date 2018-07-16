from flask import Flask
# from flask_cors import CORS
from flask_login import LoginManager

from config.appConfig import config
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__, template_folder='demo/template', static_folder='demo/static')
    # CORS(app, supports_credentials=True)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    login_manager.init_app(app)

    from .main import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
