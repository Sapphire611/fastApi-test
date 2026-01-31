from fastapi import APIRouter
from app.api.v1.endpoints import health, users

api_router = APIRouter()

# Health check
api_router.include_router(health.router, tags=["health"])

# User management
api_router.include_router(users.router, tags=["users"], prefix="/users")
