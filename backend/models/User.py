from sqlalchemy import Boolean, Column, String
from typing import ClassVar, cast

from config import settings
from .Base import BaseModel

class User(BaseModel):
    """
    User model representing a user in the system.
    """

    __tablename__: ClassVar[str] = "users"

    email = Column(String(settings.EMAIL_MAX_LENGTH), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        """Return a string representation of the user instance."""
        return f"<User(id={self.id}, email={self.email})>"

    @property
    def is_authenticated(self) -> bool:
        """Check if the user is authenticated."""
        return cast(bool, self.is_active)