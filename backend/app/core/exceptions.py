class AppException(Exception):
    """Base application exception."""

    def __init__(self, code: str, message: str, status_code: int = 500, details=None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class ValidationError(AppException):
    """Validation failed."""

    def __init__(self, message: str = "Validation error"):
        super().__init__("VALIDATION_ERROR", message, 400)


class UnauthorizedError(AppException):
    """Authentication failed."""

    def __init__(self, message: str = "Invalid credentials"):
        super().__init__("INVALID_CREDENTIALS", message, 401)


class ForbiddenError(AppException):
    """Authorization failed."""

    def __init__(self, message: str = "Permission denied"):
        super().__init__("UNAUTHORIZED", message, 403)


class NotFoundError(AppException):
    """Resource not found."""

    def __init__(self, resource: str = "Resource"):
        message = f"{resource} not found"
        super().__init__("RESOURCE_NOT_FOUND", message, 404)


class ConflictError(AppException):
    """Resource conflict."""

    def __init__(self, message: str = "Resource already exists"):
        super().__init__("CONFLICT", message, 409)


class ServerError(AppException):
    """Server error."""

    def __init__(self, message: str = "Internal server error"):
        super().__init__("SERVER_ERROR", message, 500)


class AIError(AppException):
    """AI provider error."""

    def __init__(self, message: str = "AI provider error"):
        super().__init__("AI_ERROR", message, 500)
