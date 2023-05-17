import click
from flask import Flask

from flask_user_auth.database import create_tables


@click.command
def init_db() -> None:
    """Initialize the database."""
    create_tables()
    click.echo('Initialized the database.')


def init_app(app: Flask) -> None:
    app.cli.add_command(init_db)
