from fastapi import APIRouter
from ..models.responses import HealthResponse
from ..config import settings

router = APIRouter(prefix="/health", tags=["health"])

@router.get("", response_model=HealthResponse)
def healthcheck():
    return {"status": "ok", "service": settings.app.name}
