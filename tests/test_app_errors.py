import pytest

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_register_error_renders_form(client):
    response = client.post(
        '/create',
        data={'username': 'alice', 'password1': 'abc', 'password2': 'def'},
        follow_redirects=False,
    )

    assert response.status_code == 200
    assert b'Create account' in response.data
    assert b'Passwords do not match' in response.data


def test_login_error_renders_form(client):
    response = client.post(
        '/login',
        data={'username': 'no-such-user', 'password': 'wrong'},
        follow_redirects=False,
    )

    assert response.status_code == 200
    assert b'Sign in' in response.data
    assert b'Invalid username or password' in response.data
