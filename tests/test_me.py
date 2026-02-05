def test_get_current_user(client):
    register_payload = {"email": "me@example.com", "password": "password123"}
    r = client.post("/auth/register", json=register_payload)
    assert r.status_code == 201

    login = client.post("/auth/login", json=register_payload)
    token = login.json()["access_token"]

    resp = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert resp.status_code == 200
    assert resp.json()["email"] == "me@example.com"


def test_get_current_user_without_token_returns_401(client):
    resp = client.get("/auth/me")
    assert resp.status_code == 401