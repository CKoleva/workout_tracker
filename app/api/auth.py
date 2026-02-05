from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.user import UserCreate, UserRead
from app.db.repositories.user import create_user, get_user_by_email
from app.core.security import verify_password, create_access_token
from app.schemas.auth import LoginRequest, Token
from app.core.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    existing = get_user_by_email(db, payload.email)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = create_user(db, payload.email, payload.password)
    return user

@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> Token:
    user = get_user_by_email(db, payload.email)
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect email or password",
            headers = {"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(subject=user.email)
    return Token(access_token=token, token_type="bearer")

@router.get("/me", response_model=UserRead)
def read_current_user(current_user = Depends(get_current_user)):
    return current_user