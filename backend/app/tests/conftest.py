"""Test configuration and fixtures."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.base import Base
from app.database import session

# Import models to ensure they're registered with Base
from app.models.announcement import Announcement  # noqa: F401
from app.models.school import School  # noqa: F401


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
    with TestClient(app) as test_client:
        yield test_client


# Import app AFTER patching database
from app.main import app  # noqa: F401, E402
