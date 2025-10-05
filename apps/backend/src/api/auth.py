from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.models.user import User
from src.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    get_user_by_email
)

router = APIRouter(prefix="/auth", tags=["auth"])

# ----------- Schemas -----------

class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ----------- Routes -----------

@router.post("/register", response_model=TokenResponse)
def register_user(request: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user and return a JWT token."""
    existing_user = get_user_by_email(db, request.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user = User(email=request.email, hashed_password=hash_password(request.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.email})
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return a JWT token."""
    user = get_user_by_email(db, request.email)
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return TokenResponse(access_token=token)


@router.get("/me")
def get_me(token: str):
    """Simple placeholder route for verifying token (to be improved later)."""
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")
    return {"message": "Token received", "token": token}