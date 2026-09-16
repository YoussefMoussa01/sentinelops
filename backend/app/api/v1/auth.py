"""Authentication API endpoints."""
from collections import defaultdict
from time import monotonic

from fastapi import APIRouter, Depends, HTTPException, Request, status, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.core import (
    get_settings,
    UnauthorizedError,
    create_access_token,
    create_refresh_token,
    decode_token,
    ConflictError,
)
from app.schemas import (
    LoginRequest,
    RegisterRequest,
    LoginResponse,
    UserResponse,
    TokenResponse,
    UserCreate,
)
from app.services import UserService
from app.api.dependencies import ROLE_PERMISSIONS
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()

# Process-local guard for development and single-instance deployments. A shared
# store (Redis/API gateway) should replace this when running multiple workers.
_auth_failures: dict[tuple[str, str], list[float]] = defaultdict(list)


def _check_auth_rate_limit(request: Request, action: str) -> tuple[str, str]:
    key = (request.client.host if request.client else "unknown", action)
    now = monotonic()
    window = settings.AUTH_RATE_LIMIT_WINDOW_SECONDS
    recent = [timestamp for timestamp in _auth_failures[key] if now - timestamp < window]
    _auth_failures[key] = recent
    if len(recent) >= settings.AUTH_RATE_LIMIT_ATTEMPTS:
        retry_after = max(1, int(window - (now - recent[0])))
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many authentication attempts. Try again later.",
            headers={"Retry-After": str(retry_after)},
        )
    return key


def _record_auth_failure(key: tuple[str, str]) -> None:
    _auth_failures[key].append(monotonic())


def _clear_auth_failures(key: tuple[str, str]) -> None:
    _auth_failures.pop(key, None)

def user_access(user):
    return {
        "role": user.role,
        "roles": [user.role],
        "permissions": sorted(ROLE_PERMISSIONS.get(user.role, set())),
    }


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
async def login(request: Request, login_req: LoginRequest, db: Session = Depends(get_db)):
    """Login endpoint - authenticate with username and password."""
    rate_key = _check_auth_rate_limit(request, "login")
    try:
        # Authenticate user
        user = UserService.authenticate_user(db, login_req.username, login_req.password)
        _clear_auth_failures(rate_key)

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
                **user_access(user),
            },
            token_type="bearer",
        )
    except UnauthorizedError as e:
        _record_auth_failure(rate_key)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )
    except Exception as e:
        logger.exception("Login failed unexpectedly")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed",
        )


@router.post("/register", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
async def register(request: Request, register_req: RegisterRequest, db: Session = Depends(get_db)):
    """Create a viewer account and sign the user in."""
    rate_key = _check_auth_rate_limit(request, "register")
    try:
        user = UserService.create_user(
            db,
            UserCreate(
                username=register_req.username,
                email=register_req.email,
                password=register_req.password,
                role="VIEWER",
            ),
        )
        tokens = create_tokens(user.id)
        _clear_auth_failures(rate_key)
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
                **user_access(user),
            },
            token_type="bearer",
        )
    except ConflictError as exc:
        _record_auth_failure(rate_key)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.message) from exc


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
            role=user.role,
            roles=[user.role],
            permissions=sorted(ROLE_PERMISSIONS.get(user.role, set())),
        )
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )
