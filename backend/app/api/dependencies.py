"""API dependencies."""
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.core.security import decode_token
from app.repositories.user_repository import UserRepository

ROLE_PERMISSIONS = {
    "SUPER_ADMIN": {
        "view_alerts", "manage_alerts", "view_investigations", "manage_investigations",
        "view_users", "view_devices", "manage_devices", "view_logs", "use_ai_agent", "manage_users",
        "view_ip_addresses", "manage_ip_addresses", "manage_super_admins",
    },
    "SOC_ADMIN": {
        "view_alerts", "manage_alerts", "view_investigations", "manage_investigations",
        "view_users", "view_devices", "manage_devices", "view_logs", "use_ai_agent", "manage_users",
        "view_ip_addresses", "manage_ip_addresses",
    },
    "SECURITY_ANALYST": {
        "view_alerts", "manage_alerts", "view_investigations", "manage_investigations",
        "view_devices", "manage_devices", "view_logs", "use_ai_agent",
        "view_ip_addresses", "manage_ip_addresses",
    },
    "INVESTIGATOR": {
        "view_alerts", "manage_alerts", "view_investigations", "manage_investigations",
        "view_devices", "view_logs", "use_ai_agent", "view_ip_addresses",
    },
    "VIEWER": {"view_alerts", "view_investigations"},
}


def has_permission(user, permission: str) -> bool:
    """Return whether a user role grants a permission."""
    return permission in ROLE_PERMISSIONS.get(user.role, set())


def can_manage_role(current_user, target_role: str | None, target_user=None) -> bool:
    """Prevent non-super-admins from assigning or editing the protected role."""
    if current_user.role == "SUPER_ADMIN":
        return True
    if target_role == "SUPER_ADMIN":
        return False
    if target_user is not None and target_user.role == "SUPER_ADMIN":
        return False
    return True


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


async def get_current_user(
    token: str = Depends(get_token_from_header), db: Session = Depends(get_db)
):
    """Get current authenticated user from JWT token."""
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = UserRepository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled",
        )

    return user


def check_permission(permission: str):
    """Check if user has specific permission."""

    async def _check_permission(current_user = Depends(get_current_user)):
        if not has_permission(current_user, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return _check_permission
