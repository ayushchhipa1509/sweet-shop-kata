import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend import auth
from backend.models import Sweet, User

# Marks all tests in this file to use the "client" and "session" fixtures
pytestmark = pytest.mark.usefixtures("client")


def test_get_sweets_empty(client: TestClient, session: Session):
    """Test 1: GET /sweets -> Expect empty list (public endpoint)"""
    response = client.get("/sweets")
    assert response.status_code == 200
    data = response.json()
    assert data == []


def test_create_sweet_unauthorized(client: TestClient, session: Session):
    """Test 2: POST /sweets without token -> Expect 401 (Unauthorized)"""
    response = client.post(
        "/sweets",
        json={"name": "Gulab Jamun", "category": "Classic", "price": 15.0, "quantity": 50}
    )
    assert response.status_code == 401


def test_create_sweet_authorized(client: TestClient, session: Session):
    """Test 3: POST /sweets with token -> Expect 201 (Created)"""
    # Create a user and get token
    password = "password123"
    hashed_password = auth.get_password_hash(password)
    user = User(username="adminuser", email="admin@example.com", 
               password_hash=hashed_password, role="admin")
    session.add(user)
    session.commit()

    # Login to get token
    login_response = client.post(
        "/auth/login",
        data={"username": "adminuser", "password": password},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    token = login_response.json()["access_token"]

    # Create sweet with token
    response = client.post(
        "/sweets",
        json={"name": "Gulab Jamun", "category": "Classic", "price": 15.0, "quantity": 50},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Gulab Jamun"
    assert data["price"] == 15.0
    assert data["quantity"] == 50
    assert "id" in data


def test_purchase_sweet(client: TestClient, session: Session):
    """Test 4: POST /sweets/:id/purchase -> Expect quantity to decrease by 1"""
    # Create a sweet first
    sweet = Sweet(name="Ladoo", category="Classic", price=10.0, quantity=100)
    session.add(sweet)
    session.commit()
    session.refresh(sweet)
    sweet_id = sweet.id
    initial_quantity = sweet.quantity

    # Purchase the sweet (public endpoint)
    response = client.post(f"/sweets/{sweet_id}/purchase")
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == initial_quantity - 1

    # Verify in database
    updated_sweet = session.get(Sweet, sweet_id)
    assert updated_sweet.quantity == initial_quantity - 1


def test_purchase_sweet_out_of_stock(client: TestClient, session: Session):
    """Test: Purchase sweet with quantity 0 should fail"""
    # Create a sweet with 0 quantity
    sweet = Sweet(name="Out of Stock", category="Classic", price=10.0, quantity=0)
    session.add(sweet)
    session.commit()
    session.refresh(sweet)
    sweet_id = sweet.id

    # Try to purchase
    response = client.post(f"/sweets/{sweet_id}/purchase")
    assert response.status_code == 400
    assert "out of stock" in response.json()["detail"].lower()


def test_get_sweets_list(client: TestClient, session: Session):
    """Test: GET /sweets returns list of all sweets"""
    # Create some sweets
    sweet1 = Sweet(name="Ladoo", category="Classic", price=10.0, quantity=100)
    sweet2 = Sweet(name="Gulab Jamun", category="Classic", price=15.0, quantity=50)
    session.add(sweet1)
    session.add(sweet2)
    session.commit()

    # Get all sweets
    response = client.get("/sweets")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    names = [s["name"] for s in data]
    assert "Ladoo" in names
    assert "Gulab Jamun" in names
