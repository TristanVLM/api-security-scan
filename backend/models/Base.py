from typing import Any
from sqlalchemy import Column, DateTime, Integer
from datetime import datetime, timezone
from sqlalchemy.ext.declarative import declared_attr

from core.database import Base

class BaseModel(Base):
    """
    Abstract base class for all models, providing common fields and functionality.
    """

    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Generate the table name based on the class name."""
        return cls.__name__.lower()

    def to_dict(self) -> dict[str, Any]:
        """Convert the model instance to a dictionary."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def update(self, **kwargs: Any) -> None:
        """Update the model instance with the provided keyword arguments."""
        for key, value in kwargs.items():
              if hasattr(self, key):
                  setattr(self, key, value)
        self.updated_at = datetime.now(timezone.utc)

    def __repr__(self) -> str:
        """Return a string representation of the model instance."""
        return f"<{self.__class__.__name__}(id={self.id})>"

