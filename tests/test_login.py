def test_login_success_returns_token(client):
    register_payload = {"email": "login@example.com", "password": "password123"}
    r = client.post("/auth/register", json=register_payload)
    assert r.status_code == 201

    login_payload = {"email": "login@example.com", "password": "password123"}
    resp = client.post("/auth/login", json=login_payload)

    assert resp.status_code == 200
    data = resp.json()
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 20


def test_login_wrong_password_returns_401(client):
    register_payload = {"email": "wrongpass@example.com", "password": "password123"}
    r = client.post("/auth/register", json=register_payload)
    assert r.status_code == 201

    resp = client.post(
        "/auth/login",
        json={"email": "wrongpass@example.com", "password": "nope"},
    )
    assert resp.status_code == 401
    assert "detail" in resp.json()


def test_login_unknown_email_returns_401(client):
    resp = client.post(
        "/auth/login",
        json={"email": "missing@example.com", "password": "password123"},
    )
    assert resp.status_code == 401
    assert "detail" in resp.json()