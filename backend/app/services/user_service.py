"""User service for business logic."""
from sqlalchemy.orm import Session
from app.core import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    UnauthorizedError,
    NotFoundError,
)
from app.models import User
from app.repositories import UserRepository
from app.schemas import UserResponse, UserCreate, UserUpdate


class UserService:
    """Service layer for user operations."""

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> User:
        """Authenticate user with username and password."""
        user = UserRepository.get_by_username(db, username)
        if not user or not verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid username or password")
        if not user.is_active:
            raise UnauthorizedError("User account is disabled")
        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> User:
        """Get user by ID."""
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise NotFoundError("User")
        return user

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User:
        """Get user by username."""
        user = UserRepository.get_by_username(db, username)
        if not user:
            raise NotFoundError("User")
        return user

    @staticmethod
    def create_user(db: Session, user_create: UserCreate) -> User:
        """Create a new user."""
        return UserRepository.create(
            db,
            username=user_create.username,
            email=user_create.email,
            password=user_create.password,
        )

    @staticmethod
    def update_user(db: Session, user_id: str, user_update: UserUpdate) -> User:
        """Update user."""
        return UserRepository.update(
            db,
            user_id,
            email=user_update.email,
            is_active=user_update.is_active,
        )

    @staticmethod
    def delete_user(db: Session, user_id: str) -> None:
        """Delete user."""
        UserRepository.delete(db, user_id)

    @staticmethod
    def list_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
        """List all users."""
        return UserRepository.get_all(db, skip, limit)
