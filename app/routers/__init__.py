from fastapi import APIRouter
from .orders.router import router as orders_router

api = APIRouter(prefix="/api/v1")

api.include_router(orders_router)
