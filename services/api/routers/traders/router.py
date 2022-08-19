# FastAPI
from fastapi import APIRouter, Depends, status, Body, Query, Path
from fastapi.security import OAuth2PasswordRequestForm

# Interaction with the database
from sqlalchemy.orm import Session
from schemas.trader import TraderUpdate
from database import get_db
from .db import (
    createTrader,
    traderAuth,
    deleteTrader,
    getTrader,
    getTraders,
    updateTrader,
)

# Schemas
from schemas import TraderInDB, TraderResponse, Token, Login, TraderOut

# Utils
from utils.OAuth import oauth2_schema

router = APIRouter(prefix="/traders", tags=["Traders"])


# ----------------------
#  Login JWT to account
# ----------------------
@router.post(path="/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(
    db: Session = Depends(get_db), login: OAuth2PasswordRequestForm = Depends()
):
    credentials = Login(username=login.username, password=login.password)
    return traderAuth(db, credentials)


# ------------------
#  Signup a account
# ------------------
@router.post(
    path="/singup",
    response_model=TraderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a user",
)
async def sign_up(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_schema),
    userRequest: TraderInDB = Body(...),
):
    return createTrader(db, token, userRequest)


# ---------------
# Delete a Trader
# ---------------
@router.delete(
    path="/delete/{username}",
    status_code=status.HTTP_200_OK,
    response_model=TraderResponse,
    summary="Delete a user",
)
async def delete_trader(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_schema),
    username: str = Path(...),
):
    return deleteTrader(db, token, username)


# ------------
#  Get a user
# ------------
@router.get(
    path="/{username}",
    status_code=status.HTTP_200_OK,
    summary="Get a User",
    response_model=TraderResponse,
)
async def get_a_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_schema),
    username: str = Path(...),
):
    return getTrader(db, token, username)


# --------------
#  Get all user
# --------------
@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    summary="Get Users",
    response_model=list[TraderOut],
)
async def get_users(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_schema),
    page: int = Query(default=0),
    limit: int = Query(default=10),
):
    return getTraders(db, token, page, limit)


# ----------------
#  Update user
# ----------------
@router.put(
    path="/update/user/{username}",
    status_code=status.HTTP_200_OK,
    summary="update a user's information",
)
async def update_data_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_schema),
    userRequest: TraderUpdate = Body(...),
    username: str = Path(...),
):
    return updateTrader(db, token, userRequest, username)
