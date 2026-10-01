from tests.conftest import auth_headers


def test_list_users_requires_auth(client):
    response = client.get("/users/")
    assert response.status_code in (401, 403)


def test_list_users_forbidden_for_customer(client, customer):
    headers = auth_headers(client, "customer@example.com", "custpass")
    response = client.get("/users/", headers=headers)
    assert response.status_code == 403


def test_list_users_ok_for_superadmin(client, superadmin, customer):
    headers = auth_headers(client, "root@example.com", "rootpass")
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200
    emails = {u["email"] for u in response.json()}
    assert "root@example.com" in emails
    assert "customer@example.com" in emails
    for user in response.json():
        assert "password_hash" not in user
        assert "password" not in user


def test_create_user(client, superadmin):
    headers = auth_headers(client, "root@example.com", "rootpass")
    response = client.post(
        "/users/",
        headers=headers,
        json={
            "name": "Ana",
            "email": "ana@example.com",
            "password": "anapass",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "ana@example.com"
    assert body["name"] == "Ana"
    assert "id" in body


def test_create_user_duplicate_email(client, superadmin, customer):
    headers = auth_headers(client, "root@example.com", "rootpass")
    response = client.post(
        "/users/",
        headers=headers,
        json={
            "name": "Dup",
            "email": "customer@example.com",
            "password": "whatever",
        },
    )
    assert response.status_code == 409


def test_get_user_not_found(client, superadmin):
    headers = auth_headers(client, "root@example.com", "rootpass")
    response = client.get("/users/9999", headers=headers)
    assert response.status_code == 404


def test_update_user(client, superadmin, customer):
    headers = auth_headers(client, "root@example.com", "rootpass")
    response = client.put(
        f"/users/{customer.id}",
        headers=headers,
        json={"name": "New Name", "email": "new@example.com"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"
    assert response.json()["email"] == "new@example.com"


def test_delete_user(client, superadmin, customer):
    headers = auth_headers(client, "root@example.com", "rootpass")
    response = client.delete(f"/users/{customer.id}", headers=headers)
    assert response.status_code == 204
    response = client.get(f"/users/{customer.id}", headers=headers)
    assert response.status_code == 404


def test_new_user_can_login(client, superadmin):
    headers = auth_headers(client, "root@example.com", "rootpass")
    created = client.post(
        "/users/",
        headers=headers,
        json={
            "name": "Login Me",
            "email": "loginme@example.com",
            "password": "loginpass",
        },
    )
    assert created.status_code == 201
    login = client.post(
        "/auth/login",
        json={"email": "loginme@example.com", "password": "loginpass"},
    )
    assert login.status_code == 200
