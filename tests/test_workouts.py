from datetime import datetime, timezone, timedelta


def auth_headers(client, email="w@example.com", password="password123"):
    client.post("/auth/register", json={"email": email, "password": password})
    login = client.post("/auth/login", json={"email": email, "password": password})
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_workout(client):
    headers = auth_headers(client)

    payload = {"type": "running", "duration": 30, "calories": 250}
    resp = client.post("/workouts/", json=payload, headers=headers)

    assert resp.status_code == 200
    data = resp.json()
    assert data["type"] == "running"
    assert data["duration"] == 30
    assert data["calories"] == 250
    assert "id" in data


def test_list_workouts_only_for_current_user(client):
    headers_1 = auth_headers(client, email="u1@example.com")
    headers_2 = auth_headers(client, email="u2@example.com")

    client.post(
        "/workouts/",
        json={"type": "cycling", "duration": 40, "calories": 300},
        headers=headers_1,
    )

    resp_1 = client.get("/workouts/", headers=headers_1)
    resp_2 = client.get("/workouts/", headers=headers_2)

    assert resp_1.status_code == 200
    assert resp_2.status_code == 200

    assert len(resp_1.json()) == 1
    assert len(resp_2.json()) == 0

def test_workout_filter_by_date(client):
    headers = auth_headers(client)

    old_date = datetime.now(timezone.utc) - timedelta(days=10)
    new_date = datetime.now(timezone.utc)

    client.post(
        "/workouts/",
        json={"type": "old", "duration": 10, "calories": 100, "date": old_date.isoformat()},
        headers=headers,
    )

    client.post(
        "/workouts/",
        json={"type": "new", "duration": 20, "calories": 200, "date": new_date.isoformat()},
        headers=headers,
    )

    resp = client.get(
    "/workouts/",
    params={
        "from_date": new_date.isoformat(),
        "to_date": new_date.isoformat(),
    },
    headers=headers,
    )

    assert resp.status_code == 200
    assert len(resp.json()) == 1
    assert resp.json()[0]["type"] == "new"