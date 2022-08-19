# FastAPI
from fastapi import APIRouter

# Environment Variables
from config import APP_VERSION

# Routes
from .assets.router import router as assets_router
from .traders.router import router as traders_router

api = APIRouter(prefix=f"/api/v{APP_VERSION}")
api.include_router(traders_router)

assets = APIRouter(prefix="/assets", tags=["Assets"])
assets.include_router(assets_router)
