from flask import Flask
from flask_login import LoginManager

from flask_user_auth.database import User, db

login_manager = LoginManager()


def load_user(user_id: str) -> User | None:
    return db.session.get(User, int(user_id))


def init_app(app: Flask) -> None:
    login_manager.init_app(app)
    login_manager.user_loader(load_user)
