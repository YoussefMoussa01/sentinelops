"""API exception handlers."""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.exceptions import AppException
from app.core.logging import get_logger
from app.core.config import get_settings

logger = get_logger("api")


def cors_headers(request: Request) -> dict[str, str]:
    """Keep CORS headers on application-level error responses."""
    origin = request.headers.get("origin")
    if origin and origin in get_settings().cors_origins_list:
        return {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
            "Vary": "Origin",
        }
    return {}


def add_exception_handlers(app: FastAPI):
    """Add exception handlers to FastAPI app."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        """Handle application exceptions."""
        logger.warning(f"AppException: {exc.code} - {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": exc.details,
                },
                "meta": {"timestamp": __import__("datetime").datetime.now(
                    __import__("datetime").timezone.utc
                ).isoformat()},
            },
            headers=cors_headers(request),
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle unexpected exceptions."""
        logger.error(f"Unexpected exception: {str(exc)}", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error": {
                    "code": "SERVER_ERROR",
                    "message": "Internal server error",
                    "details": None,
                },
                "meta": {"timestamp": __import__("datetime").datetime.now(
                    __import__("datetime").timezone.utc
                ).isoformat()},
            },
            headers=cors_headers(request),
        )
