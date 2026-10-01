from tests.conftest import create_user


def test_login_success(client, customer):
    response = client.post(
        "/auth/login",
        json={"email": "customer@example.com", "password": "custpass"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert isinstance(body["access_token"], str)
    assert body["access_token"]


def test_login_wrong_password(client, customer):
    response = client.post(
        "/auth/login",
        json={"email": "customer@example.com", "password": "wrong"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales inválidas"


def test_login_unknown_email(client):
    response = client.post(
        "/auth/login",
        json={"email": "nobody@example.com", "password": "whatever"},
    )
    assert response.status_code == 401


def test_login_invalid_email_format(client):
    response = client.post(
        "/auth/login",
        json={"email": "not-an-email", "password": "whatever"},
    )
    assert response.status_code == 422


def test_login_user_without_password_hash_returns_401(client, db_session):
    create_user(
        db_session,
        email="nopass@example.com",
        with_password=False,
    )
    response = client.post(
        "/auth/login",
        json={"email": "nopass@example.com", "password": "secret123"},
    )
    assert response.status_code == 401
