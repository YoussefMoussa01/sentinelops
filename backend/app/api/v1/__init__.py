"""API v1 routes."""
from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.admin import router as admin_router
from app.api.v1.alerts import router as alerts_router
from app.api.v1.investigations import router as investigations_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.devices import router as devices_router

router = APIRouter()

# Include sub-routers
router.include_router(auth_router)
router.include_router(admin_router)
router.include_router(alerts_router)
router.include_router(investigations_router)
router.include_router(dashboard_router)
router.include_router(devices_router)


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
