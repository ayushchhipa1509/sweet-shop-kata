from sqlmodel import Session
from backend.models import Sweet, User


def test_create_sweet(session: Session):
    """Test that we can create a Sweet object and save it to the database."""
    # Red phase: This test should verify the Sweet model works
    sweet = Sweet(name="Ladoo", price=10, quantity=100, category="Classic")

    session.add(sweet)
    session.commit()
    session.refresh(sweet)

    # Assert that sweet.id is not None (proves it was saved to DB)
    assert sweet.id is not None
    assert sweet.name == "Ladoo"
    assert sweet.price == 10
    assert sweet.quantity == 100
    assert sweet.category == "Classic"


def test_create_user(session: Session):
    """Test that we can create a User object and save it to the database."""
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash="hashed_password_here",
        role="user"
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Assert that user.id is not None (proves it was saved to DB)
    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.role == "user"
    assert user.password_hash == "hashed_password_here"
