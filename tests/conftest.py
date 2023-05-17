import pytest
from flask import Flask
from flask.testing import FlaskCliRunner

from flask_user_auth import create_app
from flask_user_auth.database import create_tables


@pytest.fixture
def app() -> Flask:
    app_ = create_app(TESTING=True, SQLALCHEMY_DATABASE_URI='sqlite://')
    with app_.app_context():
        create_tables()

    return app_


@pytest.fixture
def runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()
