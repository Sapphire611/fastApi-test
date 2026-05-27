from fastapi import APIRouter
from app.schemas.health import HealthCheck

router = APIRouter()

@router.get("/health", response_model=HealthCheck)
def health_check():
    return {"status": "ok", "version": "1.0.0"}
