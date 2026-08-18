from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema."""

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    """User creation schema."""

    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """User update schema."""

    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """User response schema."""

    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RoleResponse(BaseModel):
    """Role response schema."""

    id: str
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class PermissionResponse(BaseModel):
    """Permission response schema."""

    id: str
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class PaginationParams(BaseModel):
    """Pagination parameters."""

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class PaginationMeta(BaseModel):
    """Pagination metadata."""

    page: int
    page_size: int
    total: int
    total_pages: int


class ApiResponse(BaseModel):
    """Standard API response."""

    status: str
    data: Optional[dict] = None
    error: Optional[dict] = None
    meta: Optional[dict] = None


class PaginatedResponse(ApiResponse):
    """Paginated API response."""

    pass
