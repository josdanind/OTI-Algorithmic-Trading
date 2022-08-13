# FastAPI
from fastapi import APIRouter, Depends

# Databas
from sqlalchemy.orm import Session
from ...database import get_db


router = APIRouter(prefix="/orders")


@router.get("")
async def price(db: Session = Depends(get_db)):
    return {"BTC_USDT": 50000}
