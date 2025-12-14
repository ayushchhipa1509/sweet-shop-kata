import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend import auth
from backend.models import User

# Marks all tests in this file to use the "client" and "session" fixtures
pytestmark = pytest.mark.usefixtures("client")


def test_register_user(client: TestClient, session: Session):
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "email": "test@example.com",
              "password": "password123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "password_hash" not in data  # Ensure password hash is not returned


def test_register_existing_user(client: TestClient, session: Session):
    # First, create a user directly in the DB
    user = User(username="existinguser",
                email="existing@example.com", password_hash="somehash")
    session.add(user)
    session.commit()

    # Now, try to register with the same username
    response = client.post(
        "/auth/register",
        json={"username": "existinguser",
              "email": "new@example.com", "password": "password123"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"


def test_login_for_access_token(client: TestClient, session: Session):
    # Create user first
    password = "password123"
    hashed_password = auth.get_password_hash(password)
    user = User(username="loginuser", email="login@example.com",
                password_hash=hashed_password)
    session.add(user)
    session.commit()

    # Attempt to login
    response = client.post(
        "/auth/login",
        data={"username": "loginuser", "password": password},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_with_wrong_password(client: TestClient, session: Session):
    # Create user first
    password = "password123"
    hashed_password = auth.get_password_hash(password)
    user = User(username="wrongpassuser",
                email="wrongpass@example.com", password_hash=hashed_password)
    session.add(user)
    session.commit()

    # Attempt to login with wrong password
    response = client.post(
        "/auth/login",
        data={"username": "wrongpassuser", "password": "wrongpassword"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"
