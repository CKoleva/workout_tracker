from sqlalchemy.orm import Session

from app.db.models.user import User


def auth_headers(client, email="admin_test@example.com", password="password123"):
    client.post("/auth/register", json={"email": email, "password": password})
    login = client.post("/auth/login", json={"email": email, "password": password})
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def make_user_admin(db_session: Session, email: str):
    user = db_session.query(User).filter(User.email == email).first()
    assert user is not None
    user.role = "admin"
    db_session.commit()


def test_admin_users_requires_admin(client):
    headers = auth_headers(client, email="user1@example.com")

    resp = client.get("/admin/users", headers=headers)
    assert resp.status_code == 403


def test_admin_users_allows_admin(client, db_session):
    headers = auth_headers(client, email="admin@example.com")
    make_user_admin(db_session, "admin@example.com")

    auth_headers(client, email="user2@example.com")

    resp = client.get("/admin/users", headers=headers)
    assert resp.status_code == 200
    data = resp.json()

    assert any(u["email"] == "admin@example.com" for u in data)
    assert any(u["email"] == "user2@example.com" for u in data)
