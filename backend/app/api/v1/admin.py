"""Admin API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core import NotFoundError, ConflictError
from app.schemas import UserCreate, UserResponse, UserUpdate, PaginationParams
from app.services import UserService
from app.models import User

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=dict)
async def list_users(
    db: Session = Depends(get_db),
    page: int = 1,
    page_size: int = 20,
):
    """List all users (admin only)."""
    skip = (page - 1) * page_size
    users = UserService.list_users(db, skip=skip, limit=page_size)
    total = db.query(User).count()
    total_pages = (total + page_size - 1) // page_size
    
    return {
        "status": "success",
        "data": [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "is_active": u.is_active,
                "created_at": u.created_at.isoformat(),
                "updated_at": u.updated_at.isoformat(),
            }
            for u in users
        ],
        "meta": {
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": total_pages,
            }
        },
    }


@router.post("/users", response_model=dict)
async def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
    """Create a new user (admin only)."""
    try:
        user = UserService.create_user(db, user_create)
        return {
            "status": "success",
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat(),
            },
        }
    except ConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.patch("/users/{user_id}", response_model=dict)
async def update_user(
    user_id: str, user_update: UserUpdate, db: Session = Depends(get_db)
):
    """Update user (admin only)."""
    try:
        user = UserService.update_user(db, user_id, user_update)
        return {
            "status": "success",
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat(),
            },
        }
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.delete("/users/{user_id}")
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    """Delete user (admin only)."""
    try:
        UserService.delete_user(db, user_id)
        return {"status": "success", "message": "User deleted"}
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
