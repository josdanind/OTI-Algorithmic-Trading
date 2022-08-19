# SQLAlchemy
from sqlalchemy.orm import Session

# Database
from database.queries import check_existence

# Schemas
from schemas import Token

# Utils
from .OAuth import decode_access_token
from .http_errors import no_permissions


def validate_token(db: Session, token: Token):
    payload = decode_access_token(token)

    return check_existence(
        db, "Trader", error_message="User don't  Exists!", id=payload["id"]
    )


def check_permits(db: Session, token: Token, access_level: int):
    db_trader = validate_token(db, token)
    level = db_trader.access_level

    if level <= access_level:
        return
    else:
        raise no_permissions
