from flask import Flask

from flask_user_auth import commands, config, database, login, views


def create_app(**settings) -> Flask:
    app = Flask(__name__)
    config.init_app(app, settings)
    database.init_app(app)
    commands.init_app(app)
    login.init_app(app)
    views.init_app(app)
    return app
