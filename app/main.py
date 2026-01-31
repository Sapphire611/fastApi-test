from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.router import api_router
from app.core.database import db

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_db_client():
    """Connect to MongoDB on startup"""
    db.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close MongoDB connection on shutdown"""
    db.close()

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Scaffold. Visit /docs for documentation."}
