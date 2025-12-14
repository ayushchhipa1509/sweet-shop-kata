from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from backend import auth, models, schemas
from backend.database import get_session

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=schemas.UserPublic, status_code=status.HTTP_201_CREATED)
def register_user(user_in: schemas.UserCreate, session: Session = Depends(get_session)):
    # Check if user already exists
    user = session.exec(select(models.User).where(
        models.User.username == user_in.username)).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")

    user_by_email = session.exec(select(models.User).where(
        models.User.email == user_in.email)).first()
    if user_by_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Hash the password
    hashed_password = auth.get_password_hash(user_in.password)

    # Create new user object
    db_user = models.User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hashed_password,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(models.User).where(
        models.User.username == form_data.username)).first()
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth.create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}
