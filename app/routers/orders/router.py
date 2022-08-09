from fastapi import APIRouter

router = APIRouter(prefix="/orders")


@router.get("")
async def price():
    return {"BTC_USDT": 50000}
