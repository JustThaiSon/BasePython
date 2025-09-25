from fastapi import APIRouter

from app.api.api_healthCheck import router as health_router

router = APIRouter()

router.include_router(health_router, tags=["health-check"], prefix="/healthcheck")
