"""Validation utilities."""
from pydantic import ValidationError as PydanticValidationError
from app.core.exceptions import ValidationError


def validate_email_format(email: str) -> bool:
    """Validate email format."""
    import re

    pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    return re.match(pattern, email) is not None


def validate_username_format(username: str) -> bool:
    """Validate username format."""
    return 3 <= len(username) <= 50


def validate_password_strength(password: str) -> bool:
    """Validate password strength."""
    return len(password) >= 8


def handle_validation_error(error: PydanticValidationError) -> ValidationError:
    """Convert Pydantic validation error to AppException."""
    errors = error.errors()
    message = f"Validation error: {errors[0]['msg']}" if errors else "Validation error"
    return ValidationError(message)
