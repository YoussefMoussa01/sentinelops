"""Authentication API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.core import (
    get_settings,
    UnauthorizedError,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.schemas import (
    LoginRequest,
    LoginResponse,
    UserResponse,
    TokenResponse,
)
from app.services import UserService

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


def get_token_from_header(authorization: str = Header(None)) -> str:
    """Extract bearer token from Authorization header."""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
        )

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
        )

    return parts[1]


def create_tokens(user_id: str) -> dict:
    """Create access and refresh tokens."""
    access_token = create_access_token({"sub": user_id})
    refresh_token = create_refresh_token({"sub": user_id})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@router.post("/login", response_model=LoginResponse)
async def login(login_req: LoginRequest, db: Session = Depends(get_db)):
    """Login endpoint - authenticate with username and password."""
    try:
        # Authenticate user
        user = UserService.authenticate_user(db, login_req.username, login_req.password)

        # Create tokens
        tokens = create_tokens(user.id)

        # Return response
        return LoginResponse(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            user={
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat(),
            },
            token_type="bearer",
        )
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed",
        )


@router.post("/logout")
async def logout():
    """Logout endpoint - client-side token cleanup."""
    return {"status": "success", "message": "Logged out successfully"}


@router.post("/refresh", response_model=TokenResponse)
async def refresh_access_token(
    request_body: dict,
    db: Session = Depends(get_db),
):
    """Refresh token endpoint."""
    try:
        refresh_token = request_body.get("refresh_token")
        if not refresh_token:
            raise UnauthorizedError("Missing refresh token")

        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise UnauthorizedError("Invalid refresh token")

        user_id = payload.get("sub")
        user = UserService.get_user_by_id(db, user_id)

        tokens = create_tokens(user.id)

        return TokenResponse(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            token_type="bearer",
        )
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    db: Session = Depends(get_db),
    token: str = Depends(get_token_from_header),
):
    """Get current authenticated user info."""
    try:
        payload = decode_token(token)
        if not payload:
            raise UnauthorizedError("Invalid token")

        user_id = payload.get("sub")
        user = UserService.get_user_by_id(db, user_id)

        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )
