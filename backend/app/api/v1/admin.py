"""Admin API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core import NotFoundError, ConflictError, ForbiddenError
from app.schemas import UserCreate, UserResponse, UserUpdate, PaginationParams
from app.services import UserService
from app.models import User
from app.api.dependencies import can_manage_role, check_permission

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=dict, dependencies=[Depends(check_permission("view_users"))])
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
                "role": u.role,
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


@router.post("/users", response_model=dict, dependencies=[Depends(check_permission("manage_users"))])
async def create_user(
    user_create: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(check_permission("manage_users")),
):
    """Create a new user (admin only)."""
    try:
        if not can_manage_role(current_user, user_create.role):
            raise ForbiddenError("Only a SUPER_ADMIN can create another SUPER_ADMIN")
        user = UserService.create_user(db, user_create)
        return {
            "status": "success",
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
                "role": user.role,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat(),
            },
        }
    except ConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.patch("/users/{user_id}", response_model=dict, dependencies=[Depends(check_permission("manage_users"))])
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(check_permission("manage_users")),
):
    """Update user (admin only)."""
    try:
        target = UserService.get_user_by_id(db, user_id)
        if not can_manage_role(current_user, user_update.role, target):
            raise ForbiddenError("Only a SUPER_ADMIN can manage SUPER_ADMIN accounts")
        if current_user.id == target.id and target.role == "SUPER_ADMIN" and user_update.role != "SUPER_ADMIN":
            raise ForbiddenError("A SUPER_ADMIN cannot remove their own protected role")
        user = UserService.update_user(db, user_id, user_update)
        return {
            "status": "success",
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
                "role": user.role,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat(),
            },
        }
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.delete("/users/{user_id}", dependencies=[Depends(check_permission("manage_users"))])
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(check_permission("manage_users")),
):
    """Delete user (admin only)."""
    try:
        target = UserService.get_user_by_id(db, user_id)
        if target.role == "SUPER_ADMIN" and current_user.role != "SUPER_ADMIN":
            raise ForbiddenError("Only a SUPER_ADMIN can delete a SUPER_ADMIN account")
        if target.id == current_user.id:
            raise ForbiddenError("You cannot delete your own account")
        UserService.delete_user(db, user_id)
        return {"status": "success", "message": "User deleted"}
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.get("/users/{user_id}", response_model=dict, dependencies=[Depends(check_permission("view_users"))])
async def get_user(user_id: str, db: Session = Depends(get_db)):
    try:
        user = UserService.get_user_by_id(db, user_id)
        return {
            "status": "success",
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
                "role": user.role,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat(),
            },
        }
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
