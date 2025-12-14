from deps import get_current_admin_user, get_current_user
from database import get_session
import schemas
import models
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

import sys
from pathlib import Path
# Add parent directory (backend/) to path
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))


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
    All authenticated users can create sweets.
    """

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


@router.delete("/{sweet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sweet(
    sweet_id: int,
    session: Session = Depends(get_session),
    current_user: models.User = Depends(get_current_admin_user)
):
    """
    Delete a sweet (admin only).
    """
    sweet = session.get(models.Sweet, sweet_id)
    if not sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )

    session.delete(sweet)
    session.commit()
    return None
