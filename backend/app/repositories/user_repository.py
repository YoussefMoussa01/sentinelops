from typing import Optional
from sqlalchemy.orm import Session
from app.models.identity import User
from app.core.security import hash_password
from app.core.exceptions import NotFoundError, ConflictError


class UserRepository:
    """Repository for user database operations."""

    @staticmethod
    def create(db: Session, username: str, email: str, password: str) -> User:
        """Create a new user."""
        # Check if user already exists
        existing = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing:
            if existing.username == username:
                raise ConflictError("Username already exists")
            raise ConflictError("Email already exists")

        user = User(
            username=username,
            email=email,
            password_hash=hash_password(password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_by_id(db: Session, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_username(db: Session, username: str) -> Optional[User]:
        """Get user by username."""
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email."""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
        """Get all users."""
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def update(
        db: Session,
        user_id: str,
        email: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> User:
        """Update user."""
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise NotFoundError("User")

        if email:
            user.email = email
        if is_active is not None:
            user.is_active = is_active

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user_id: str) -> None:
        """Delete user."""
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise NotFoundError("User")

        db.delete(user)
        db.commit()
