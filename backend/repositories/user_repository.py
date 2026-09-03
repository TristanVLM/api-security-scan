from __future__ import annotations

from sqlalchemy.orm import Session
from models.User import User

class UserRepository:
    """Repository for User database operations."""
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User | None:
        """Retrieve a user by their ID."""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        """Retrieve a user by their email."""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create_user(
        db: Session, email: str, hashed_password: str, commit: bool = True
    ) -> User:
        """Create a new user in the database."""
        new_user = User(email=email, hashed_password=hashed_password)
        db.add(new_user)
        if commit:
            db.commit()
            db.refresh(new_user)
        return new_user

    @staticmethod
    def get_all_active_users(db: Session, skip: int = 0, limit: int | None = None) -> list[User]:
        """Retrieve all active users."""
        return db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()

    @staticmethod
    def update_active_status(db: Session, user_id: int, is_active: bool, commit: bool = True) -> User | None:
        """Update the active status of a user."""
        user = UserRepository.get_by_id(db, user_id)
        if user:
            setattr(user, "is_active", is_active)
            if commit:
                db.commit()
                db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int, commit: bool = True) -> bool:
        """Delete a user from the database."""
        user = UserRepository.get_by_id(db, user_id)
        if user:
            db.delete(user)
            if commit:
                db.commit()
            return True
        return False