from flask import Flask

from flask_user_auth.database import User, db


def test_user_password_hashing(faker) -> None:
    password = faker.password()
    user = User(name=faker.name(), email=faker.email(), password=password)
    assert user.is_correct_password(password)


def test_get_user_by_an_already_registered_email_should_not_return_none(
    app: Flask, faker
) -> None:
    email = faker.email()
    user = User(name=faker.name(), email=email, password=faker.password())

    with app.app_context():
        db.session.add(user)
        db.session.commit()

        assert User.get_by_email(email) is not None
