# Python
from datetime import datetime, timedelta

# pyJWT
import jwt

# Utils
from .http_errors import token_invalid, token_expired

# Schemas
from ..schemas import Token

# Database
from ..database import models

# FastAPI
from fastapi.security import OAuth2PasswordBearer

# Environment Variables
from ..config import JWT_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS, APP_VERSION

oauth2_schema = OAuth2PasswordBearer(tokenUrl=f"/api/v{APP_VERSION}/traders/login")


def create_access_token(
    db_user: models.Trader, expire_days: int = int(ACCESS_TOKEN_EXPIRE_DAYS)
):
    payload = {
        "id": db_user.id,
        "username": db_user.username,
        "access_level": db_user.access_level,
        "exp": datetime.utcnow() + timedelta(days=expire_days),
        "iat": datetime.utcnow(),
    }

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_access_token(token: Token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        if payload is None:
            raise token_invalid

        return payload
    except jwt.ExpiredSignatureError:
        raise token_expired
    except jwt.InvalidTokenError:
        raise token_invalid
