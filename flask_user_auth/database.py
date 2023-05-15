from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_tables():
    db.create_all()


def init_app(app: Flask):
    db.init_app(app)

    @app.cli.command('init-db')
    def init_db():
        """Initialize the database."""
        create_tables()


##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
