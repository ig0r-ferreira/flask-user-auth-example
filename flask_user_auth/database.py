from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


def create_tables() -> None:
    db.create_all()


def init_app(app: Flask) -> None:
    db.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.password = generate_password_hash(self.password)

    def is_correct_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)
