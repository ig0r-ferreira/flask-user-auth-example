import pytest
from faker import Faker
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner
from flask_login import FlaskLoginClient

from flask_user_auth import create_app
from flask_user_auth.database import User, create_tables, db

fake = Faker()


@pytest.fixture(scope='session', autouse=True)
def user() -> dict[str, str]:
    return {
        'name': fake.name(),
        'email': fake.email(),
        'password': fake.password(length=8),
    }


@pytest.fixture(scope='session')
def app(user: dict[str, str]) -> Flask:
    app_ = create_app(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI='sqlite://',
        WTF_CSRF_ENABLED=False,
    )
    app_.test_client_class = FlaskLoginClient

    with app_.app_context():
        create_tables()
        db.session.add(User(**user))
        db.session.commit()

    return app_


@pytest.fixture(scope='session')
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture(scope='session')
def client_with_logged_user(app: Flask) -> FlaskClient:
    with app.app_context():
        user = db.session.get(User, 1)

    return app.test_client(user=user)


@pytest.fixture
def runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()
