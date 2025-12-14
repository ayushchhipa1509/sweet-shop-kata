import pytest
from sqlmodel import SQLModel, create_engine, Session
from fastapi.testclient import TestClient

# Import models to register them with SQLModel
from backend import models  # noqa

# Use an in-memory SQLite database for testing (fresh DB for every test)
# This ensures tests don't clash with each other
sqlite_url = "sqlite:///:memory:"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})


@pytest.fixture(name="session")
def session_fixture():
    """
    Create a fresh in-memory database session for each test.
    This ensures test isolation - each test gets a clean database.
    """
    # Create fresh tables for each test
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    # Clean up after test
    SQLModel.metadata.drop_all(engine)


# Client fixture for API tests (Phase 3+) - commented out for Phase 2
# @pytest.fixture(name="client")
# def client_fixture(session: Session):
#     from backend.main import app
#     from backend.database import get_session
#
#     def get_session_override():
#         yield session
#
#     app.dependency_overrides[get_session] = get_session_override
#     client = TestClient(app)
#     yield client
#     app.dependency_overrides.clear()
