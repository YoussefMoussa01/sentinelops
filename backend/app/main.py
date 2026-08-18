"""Main FastAPI application."""
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.api.v1 import router as v1_router
from app.api.exceptions import add_exception_handlers

settings = get_settings()

# Setup logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="AI-powered cybersecurity investigation platform",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
