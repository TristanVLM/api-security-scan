from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from config import settings
from core.database import get_db
from schemas.user_schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse,
)
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: Request,
    user_create: UserCreate,
    db: Session = Depends(get_db),
) -> UserResponse:
    """Register a new user."""
    return AuthService.register_user(db, user_create)

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    request: Request,
    user_login: UserLogin,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Authenticate a user and return a JWT token."""
    return AuthService.authenticate_user(db, user_login)
