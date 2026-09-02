"""API v1 routes."""
from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.admin import router as admin_router
from app.api.v1.alerts import router as alerts_router
from app.api.v1.investigations import router as investigations_router

router = APIRouter()

# Include sub-routers
router.include_router(auth_router)
router.include_router(admin_router)
router.include_router(alerts_router)
router.include_router(investigations_router)


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
