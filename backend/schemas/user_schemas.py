from __future__ import annotations
import re
from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from config import settings

class UserCreate(BaseModel):
    """Schema for user registration request"""

    model_config = ConfigDict(from_attributes=True)

    email: EmailStr = Field(..., max_length=settings.EMAIL_MAX_LENGTH)
    password: str = Field(..., min_length=settings.PASSWORD_MIN_LENGTH, max_length=settings.PASSWORD_MAX_LENGTH)

    @field_validator("password")
    def validate_password_strength(cls, value: str) -> str:
        """Validate the password meets security requirements."""
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit.")
        return value

class UserLogin(BaseModel):
    """Schema for user login request"""

    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """Schema for user response"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime


class TokenResponse(BaseModel):
    """Schema for JWT token response"""

    access_token: str
    token_type: str = "bearer"