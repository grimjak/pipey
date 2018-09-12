import os

from flask import Flask, Blueprint
from flask_restful import Api
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt

db = MongoEngine()
app = Flask(__name__)
toolbar = DebugToolbarExtension()
bcrypt = Bcrypt()


def create_app(script_info=None):
    # core app config
    app = Flask(__name__)
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)
    # enable CORS
    CORS(app)

    db.init_app(app)
    toolbar.init_app(app)
    bcrypt.init_app(app)

    api_bp = Blueprint('api', __name__)  # split out into another file
    api = Api(api_bp)

    app.register_blueprint(api_bp, url_prefix='/api')

    # from project.api.auth import auth_blueprint
    # app.register_blueprint(auth_blueprint)

    # model
    from project.api.people import People, Person, Ping

    api.add_resource(Ping, "/ping", endpoint="ping")
    api.add_resource(People, "/people", endpoint="people")
    api.add_resource(Person, "/people/<string:_id>", endpoint="person")

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
