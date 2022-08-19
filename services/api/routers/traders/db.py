# Python
from datetime import datetime

# SQLAlchemy
from sqlalchemy.orm import Session

# Schemas
from schemas import TraderInDB, TraderUpdate
from schemas import Login, Token

# Database
from database.queries import check_existence, write_row, delete_row, get_all
from database.models import Trader

# Utils
from utils.encrypt_password import context
from utils.http_errors import incorrect_password, no_permissions
from utils.OAuth import create_access_token
from utils.validate_token import validate_token, check_permits

# ---------
#  QUERIES
# ---------
# --// Login
def traderAuth(db: Session, credentials: Login):
    db_user = check_existence(
        db,
        model="Trader",
        error_message="User Don't Exist!",
        username=credentials.username,
    )

    if context.verify(credentials.password, db_user.hashed_password):
        return {"access_token": create_access_token(db_user), "token_type": "Bearer"}
    else:
        raise incorrect_password


# --// CREATE A USER
def createTrader(db: Session, token: Token, traderSchema: TraderInDB) -> Trader:
    check_permits(db, token, 1)
    limitations = [
        ("username", "The user exists!"),
        ("email", "There is a user with that email!"),
    ]

    for field, message in limitations:
        check_existence(
            db,
            model="Trader",
            error_message=message,
            error_if_exist=True,
            **{f"{field}": eval(f"traderSchema.{field}")},
        )

    trader_dict = traderSchema.dict()
    trader_dict["hashed_password"] = trader_dict.pop("password")
    trader_dict["trader_data"]["birth_date"] = str(
        trader_dict["trader_data"]["birth_date"]
    )

    db_user = write_row(db, "Trader", with_dict=trader_dict)
    db_user.message = "Trader created!"

    return db_user


# --// DELETE A USER
def deleteTrader(db: Session, token: Token, username: str):
    check_permits(db, token, 1)

    db_user = check_existence(
        db, "Trader", error_message="User don't  Exists!", username=username
    )

    delete_row(db, "Trader", id=db_user.id)
    db_user.message = "The user was deleted!"

    return db_user


# --// GET A USER
def getTrader(db: Session, token: Token, username: str):
    db_trader = validate_token(db, token)
    is_root = db_trader.access_level == 1

    if db_trader.username == username:
        db_trader.message = "User Exists!"
        return db_trader
    elif is_root:
        db_trader = check_existence(
            db, model="Trader", error_message="User don't Exist!", username=username
        )
        db_trader.message = "User Exists!"
        return db_trader
    else:
        raise no_permissions


# --// GET ALL USER
def getTraders(db: Session, token: Token, page: str, limit: str):
    check_permits(db, token, 1)
    db_traders = get_all(db, "Trader", skip=page, limit=limit)
    return db_traders


# --// UPDATE A USER
def updateTrader(db: Session, token: Token, toUpdate: TraderUpdate, username: str):
    db_trader = validate_token(db, token)
    is_root = db_trader.access_level == 1

    if db_trader.username == username or is_root:

        db_trader = check_existence(
            db, "Trader", error_message="User don't  Exists!", username=username
        )

        to_update = toUpdate.dict()
        trader_info = ["first_name", "last_name", "birth_date"]

        for k, v in to_update.items():
            if v:
                if k in trader_info:
                    exec(f"db_trader.trader_data['{k}'] = '{v}'")
                if k != "password" and not k in trader_info:
                    exec(f"db_trader.{k} = '{v}'")
                if k == "password":
                    db_trader.set_password(v)

        db_trader.updated_at = datetime.now()
        db_trader = write_row(db, "Trader", withModel=db_trader)
        db_trader.message = "The user data was updated!"
        return db_trader
    else:
        raise no_permissions
