from ..config import APP_VERSION
from fastapi import APIRouter
from .orders.router import router as orders_router
from .traders.router import router as traders_router
from .assets.router import router as assets_router

api = APIRouter(prefix=f"/api/v{APP_VERSION}")

api.include_router(orders_router)
api.include_router(traders_router)

assets = APIRouter()

assets.include_router(assets_router)
