from http import HTTPStatus

from flask.testing import FlaskClient

from flask_user_auth.database import User


def test_accessing_homepage_should_return_status_ok(
    client: FlaskClient,
) -> None:
    response = client.get('/')
    data = response.get_data(as_text=True)

    assert response.status_code == HTTPStatus.OK
    assert 'Flask Authentication' in data
    assert 'Login' in data
    assert 'Register' in data


def test_accessing_secrets_page_without_login_should_return_unauthorized(
    client: FlaskClient,
) -> None:
    response = client.get('/secrets')

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_download_without_login_should_return_unauthorized(
    client: FlaskClient,
) -> None:
    response = client.get('/download')

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_acessing_register_page_should_return_status_ok(
    client: FlaskClient,
) -> None:
    response = client.get('/register')
    data = response.get_data(as_text=True)

    assert response.status_code == HTTPStatus.OK
    assert 'Register' in data
    assert 'Sign up' in data


def test_registering_with_an_email_already_registered_should_return_an_error_message(
    client: FlaskClient, user: dict[str, str], faker
) -> None:
    form_data = {
        'name': faker.name(),
        'email': user['email'],
        'password': faker.password(),
    }
    response = client.post('/register', data=form_data)
    data = response.get_data(as_text=True)

    assert response.status_code == HTTPStatus.OK
    assert (
        'You&#39;ve already registered with this email, please login.' in data
    )


def test_registering_with_a_non_existent_email_should_redirect_to_secrets_page(
    client: FlaskClient, faker
) -> None:
    form_data = {
        'name': faker.name(),
        'email': faker.email(),
        'password': faker.password(),
    }
    response = client.post('/register', data=form_data)

    assert response.status_code == HTTPStatus.FOUND
    assert response.headers['Location'] == '/secrets'

    with client.application.app_context():
        assert User.get_by_email(form_data.get('email')) is not None


def test_acessing_login_page_should_return_status_ok(
    client: FlaskClient,
) -> None:
    response = client.get('/login')
    data = response.get_data(as_text=True)

    assert response.status_code == HTTPStatus.OK
    assert 'Login' in data
    assert 'Sign in' in data


def test_login_with_a_non_existent_email_should_return_a_error_message(
    client: FlaskClient, faker
) -> None:
    form_data = {'email': faker.email(), 'password': faker.password()}

    response = client.post('/login', data=form_data)
    data = response.get_data(as_text=True)

    assert response.status_code == HTTPStatus.OK
    assert 'This user does not exist, please try again.' in data


def test_login_with_incorrect_password_should_return_a_error_message(
    client: FlaskClient,
    user: dict[str, str],
    faker,
) -> None:
    form_data = {'email': user['email'], 'password': faker.password()}

    response = client.post('/login', data=form_data)
    data = response.get_data(as_text=True)

    assert response.status_code == HTTPStatus.OK
    assert 'Password incorrect, please try again.' in data


def test_login_with_valid_user_should_redirect_secrets_page(
    client: FlaskClient, user: dict[str, str]
) -> None:
    form_data = user.copy()
    form_data.pop('name')

    response = client.post('/login', data=form_data)

    assert response.status_code == HTTPStatus.FOUND
    assert response.headers['Location'] == '/secrets'


def test_accessing_secrets_page_with_logged_in_user_should_display_welcome_message(
    client_with_logged_user: FlaskClient,
    user: dict[str, str],
) -> None:
    response = client_with_logged_user.get('/secrets')
    data = response.get_data(as_text=True)

    assert response.status_code == HTTPStatus.OK
    assert f'Welcome, {user["name"]}' in data
    assert 'Download Your File' in data
    assert 'Logout' in data


def test_download_with_logged_in_user_should_return_a_pdf(
    client_with_logged_user: FlaskClient,
) -> None:
    response = client_with_logged_user.get('/download')

    assert response.status_code == HTTPStatus.OK
    assert response.headers['Content-Type'] == 'application/pdf'


def test_logout_should_redirect_to_homepage(
    client_with_logged_user: FlaskClient,
) -> None:
    response = client_with_logged_user.get('/logout')

    assert response.status_code == HTTPStatus.FOUND
    assert response.headers['Location'] == '/'
