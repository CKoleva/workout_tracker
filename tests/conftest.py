import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.database import Base
from app.db.deps import get_db


@pytest.fixture(scope="session")
def engine(tmp_path_factory):
    db_file = tmp_path_factory.mktemp("data") / "test.db"

    engine = create_engine(
        f"sqlite:///{db_file}",
        connect_args={"check_same_thread": False},
    )

    Base.metadata.create_all(bind=engine)

    yield engine

    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session(engine):
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()