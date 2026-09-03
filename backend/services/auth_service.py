from __future__ import annotations

from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from config import settings
from core.security import (
    create_access_token,
    hash_password,
    verify_password,
)

from schemas.user_schemas import (
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)

from repositories.user_repository import UserRepository

class AuthService:
    """Service class for handling user authentication and registration."""

    @staticmethod
    def register_user(db: Session, user_create: UserCreate) -> UserResponse:
        """Register a new user."""
        existing_user = UserRepository.get_by_email(db, user_create.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        hashed_password = hash_password(user_create.password)
        new_user = UserRepository.create_user(db, user_create.email, hashed_password)
        return UserResponse.model_validate(new_user)

    @staticmethod
    def authenticate_user(db: Session, user_login: UserLogin) -> TokenResponse:
        """Authenticate a user and return a JWT token."""
        user = UserRepository.get_by_email(db, user_login.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(user_login.password, user.to_dict()["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not user.to_dict()["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.to_dict()["email"]}, expires_delta=access_token_expires
        )
        return TokenResponse(access_token=access_token, token_type="bearer")

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> UserResponse:
        """Retrieve a user by email."""
        user = UserRepository.get_by_email(db, email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return UserResponse.model_validate(user)