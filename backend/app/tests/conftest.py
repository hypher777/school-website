"""Test configuration and fixtures."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.base import Base
from app.database import session

# Import models to ensure they're registered with Base
from app.models.announcement import Announcement  # noqa: F401
from app.models.event import Event  # noqa: F401
from app.models.school import School  # noqa: F401
from app.models.admin import Admin  # noqa: F401


# Create test database - must use same path as app.database.session looks for
test_engine = create_engine(
    "sqlite:///./test.db",
    connect_args={"check_same_thread": False},
)

# Create all tables
Base.metadata.create_all(bind=test_engine)

# PATCH the app's database session module to use test engine
session.engine = test_engine
session.SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


@pytest.fixture(scope="function", autouse=True)
def clear_database():
    """Clear database before and after each test."""
    # Clear all data before test
    from sqlalchemy.orm import Session
    db = Session(test_engine)
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()
    db.close()

    yield

    # Clear all data after test
    db = Session(test_engine)
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()
    db.close()


@pytest.fixture(scope="function")
def client():
    """Create a test client."""
    with TestClient(app, headers={"host": "localhost"}) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def admin_client(client, clear_database):
    """Create a logged-in admin client for mutation tests."""
    from sqlalchemy.orm import Session
    from app.core.security import hash_password

    db = Session(test_engine)
    db.add(Admin(username="test-admin", password_hash=hash_password("test-password")))
    db.commit()
    db.close()
    login = client.post(
        "/api/auth/login",
        json={"username": "test-admin", "password": "test-password"},
    )
    assert login.status_code == 200
    client.headers.update(
        {"Authorization": f"Bearer {login.json()['access_token']}"}
    )
    return client


# Import app AFTER patching database
from app.main import app  # noqa: F401, E402
