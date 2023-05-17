from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from flask import Flask


def init_app(app: Flask, config: dict[str, Any]) -> None:
    load_dotenv()
    app.config.from_prefixed_env()

    if config:
        app.config.from_mapping(config)

    if not 'SQLALCHEMY_DATABASE_URI' in app.config:
        instance_folder = Path(app.instance_path)
        instance_folder.mkdir(exist_ok=True)
        database_uri = f'sqlite:///{instance_folder / "users.db"}'

        app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
