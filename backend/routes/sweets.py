from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from backend import models, schemas
from backend.database import get_session
from backend.deps import get_current_admin_user, get_current_user

router = APIRouter(prefix="/sweets", tags=["Sweets"])


@router.get("/", response_model=list[schemas.SweetPublic])
def get_sweets(session: Session = Depends(get_session)):
    """
    Get all sweets (public endpoint - no authentication required).
    """
    sweets = session.exec(select(models.Sweet)).all()
    return sweets


@router.post("/", response_model=schemas.SweetPublic, status_code=status.HTTP_201_CREATED)
def create_sweet(
    sweet_in: schemas.SweetCreate,
    session: Session = Depends(get_session),
    current_user: models.User = Depends(get_current_user)
):
    """
    Create a new sweet (requires authentication).
    Only admins can create sweets.
    """
    # Check if user is admin
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Admin role required."
        )

    # Create the sweet
    db_sweet = models.Sweet(**sweet_in.model_dump())
    session.add(db_sweet)
    session.commit()
    session.refresh(db_sweet)

    return db_sweet


@router.post("/{sweet_id}/purchase", response_model=schemas.SweetPublic)
def purchase_sweet(
    sweet_id: int,
    session: Session = Depends(get_session)
):
    """
    Purchase a sweet (public endpoint - decreases quantity by 1).
    """
    sweet = session.get(models.Sweet, sweet_id)
    if not sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )

    if sweet.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sweet is out of stock"
        )

    # Decrease quantity by 1
    sweet.quantity -= 1
    session.add(sweet)
    session.commit()
    session.refresh(sweet)

    return sweet
