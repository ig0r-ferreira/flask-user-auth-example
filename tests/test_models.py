from flask_user_auth.database import User


def test_user_password_hashing() -> None:
    password = '12345'
    user = User(name='Jonh', email='jonh@email.com', password=password)
    assert user.is_correct_password(password)
