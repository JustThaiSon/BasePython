from fastapi import APIRouter
from app.api.api_healthCheck import router as health_router
from app.api.api_auth import router as auth_router

router = APIRouter()

router.include_router(health_router, tags=["health-check"], prefix="/healthcheck")
router.include_router(auth_router, tags=["auth"], prefix="/auth")
