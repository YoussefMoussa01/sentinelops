"""Main FastAPI application."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.api.v1 import router as v1_router
from app.api.exceptions import add_exception_handlers
from app.database.session import SessionLocal
from app.models import User
from app.core.security import hash_password
from app.core.logging import get_logger

settings = get_settings()
logger = get_logger("bootstrap")

# Setup logging
setup_logging()

def bootstrap_super_admin() -> None:
    """Create the configured first super-admin without overwriting passwords."""
    if not all((settings.SUPER_ADMIN_USERNAME, settings.SUPER_ADMIN_EMAIL, settings.SUPER_ADMIN_PASSWORD)):
        return
    if len(settings.SUPER_ADMIN_PASSWORD) < 12:
        raise RuntimeError("SUPER_ADMIN_PASSWORD must contain at least 12 characters")

    db = SessionLocal()
    try:
        existing = db.query(User).filter(
            (User.username == settings.SUPER_ADMIN_USERNAME)
            | (User.email == settings.SUPER_ADMIN_EMAIL)
        ).first()
        if existing:
            if existing.username != settings.SUPER_ADMIN_USERNAME or existing.email != settings.SUPER_ADMIN_EMAIL:
                raise RuntimeError("Super-admin bootstrap username/email conflicts with an existing user")
            if existing.role != "SUPER_ADMIN" or not existing.is_active:
                existing.role = "SUPER_ADMIN"
                existing.is_active = True
                db.commit()
                logger.info("Existing bootstrap account promoted to SUPER_ADMIN: %s", existing.username)
            return

        db.add(User(
            username=settings.SUPER_ADMIN_USERNAME,
            email=settings.SUPER_ADMIN_EMAIL,
            password_hash=hash_password(settings.SUPER_ADMIN_PASSWORD),
            role="SUPER_ADMIN",
            is_active=True,
        ))
        db.commit()
        logger.info("Created configured SUPER_ADMIN account: %s", settings.SUPER_ADMIN_USERNAME)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Super-admin bootstrap failed; verify migrations are applied")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Run idempotent bootstrap work during application startup."""
    bootstrap_super_admin()
    yield


# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="AI-powered cybersecurity investigation platform",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count"],
)


# Add middleware to include timestamp in response
@app.middleware("http")
async def add_response_timestamp(request, call_next):
    """Add timestamp to all responses."""
    response = await call_next(request)
    if response.status_code >= 400:
        return response
    return response


# Include API routers
app.include_router(v1_router, prefix=settings.API_V1_PREFIX, tags=["health"])

# Add exception handlers
add_exception_handlers(app)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "SentinelOps API",
        "version": settings.API_VERSION,
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
