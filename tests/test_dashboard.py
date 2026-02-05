from datetime import datetime, timezone, timedelta


def auth_headers(client, email="dash@example.com", password="password123"):
    client.post("/auth/register", json={"email": email, "password": password})
    login = client.post("/auth/login", json={"email": email, "password": password})
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_dashboard_summary_empty(client):
    headers = auth_headers(client)

    resp = client.get("/dashboard/summary", headers=headers)
    assert resp.status_code == 200
    data = resp.json()

    assert data["total_workouts"] == 0
    assert data["total_duration"] == 0
    assert data["total_calories"] == 0


def test_dashboard_summary_counts_workouts(client):
    headers = auth_headers(client)

    client.post(
        "/workouts/",
        json={"type": "run", "duration": 30, "calories": 200},
        headers=headers,
    )
    client.post(
        "/workouts/",
        json={"type": "bike", "duration": 40, "calories": 300},
        headers=headers,
    )

    resp = client.get("/dashboard/summary", headers=headers)
    assert resp.status_code == 200
    data = resp.json()

    assert data["total_workouts"] == 2
    assert data["total_duration"] == 70
    assert data["total_calories"] == 500


def test_dashboard_summary_filters_by_date(client):
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
        "/dashboard/summary",
        params={"from_date": new_date.isoformat()},
        headers=headers,
    )

    assert resp.status_code == 200
    data = resp.json()

    assert data["total_workouts"] == 1
    assert data["total_duration"] == 20
    assert data["total_calories"] == 200