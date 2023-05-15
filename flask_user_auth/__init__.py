from flask import Flask

from flask_user_auth import config, database, views


def create_app() -> Flask:
    app = Flask(__name__)
    config.init_app(app)
    database.init_app(app)
    views.init_app(app)
    return app
