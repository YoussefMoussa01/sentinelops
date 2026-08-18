from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class LoginRequest(BaseModel):
    """Login request schema."""

    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8)


class TokenResponse(BaseModel):
    """Token response schema."""

    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


class LoginResponse(BaseModel):
    """Login response schema."""

    access_token: str
    refresh_token: Optional[str] = None
    user: dict
    token_type: str = "bearer"
