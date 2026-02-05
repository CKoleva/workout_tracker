def test_register_success(client):
    payload = {
        "email": "user@example.com",
        "password": "strongpassword123"
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["email"] == payload["email"]
    assert "hashed_password" not in data


def test_register_duplicate_email_returns_400(client):
    payload = {
        "email": "duplicate@example.com",
        "password": "password123"
    }

    first = client.post("/auth/register", json=payload)
    assert first.status_code == 201

    second = client.post("/auth/register", json=payload)
    assert second.status_code == 400

    data = second.json()
    assert "detail" in data


def test_register_invalid_email_returns_422(client):
    payload = {
        "email": "invalid-email",
        "password": "password123"
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 422


def test_register_missing_password_returns_422(client):
    payload = {
        "email": "user2@example.com"
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 422