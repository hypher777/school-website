"""Tests for admin authentication and protected mutations."""


def test_successful_login_returns_bearer_token(admin_client):
    response = admin_client.post(
        "/api/auth/login",
        json={"username": "test-admin", "password": "test-password"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert "password" not in body
    assert "password_hash" not in body


def test_invalid_login_returns_401(admin_client):
    response = admin_client.post(
        "/api/auth/login",
        json={"username": "test-admin", "password": "wrong-password"},
    )
    assert response.status_code == 401


def test_public_get_endpoints_do_not_require_authentication(client):
    assert client.get("/api/school").status_code == 404
    assert client.get("/api/announcements").status_code == 200
    assert client.get("/api/events").status_code == 200


def test_protected_endpoint_without_authentication(client):
    response = client.post(
        "/api/events",
        json={
            "title": "Restricted",
            "event_date": "2026-06-15T10:30:00",
        },
    )
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_protected_endpoint_with_valid_token(admin_client):
    response = admin_client.post(
        "/api/events",
        json={
            "title": "Authorized",
            "event_date": "2026-06-15T10:30:00",
        },
    )
    assert response.status_code == 201


def test_protected_endpoint_with_invalid_token(client):
    client.headers["Authorization"] = "Bearer not-a-valid-token"
    response = client.post(
        "/api/events",
        json={
            "title": "Rejected",
            "event_date": "2026-06-15T10:30:00",
        },
    )
    assert response.status_code == 401


def test_password_hash_is_not_returned_by_api(admin_client):
    response = admin_client.get("/api/events")
    assert response.status_code == 200
    assert all("password_hash" not in item for item in response.json())
