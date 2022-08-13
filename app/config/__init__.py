from os import environ

# APP
APP_VERSION = environ["APP_VERSION"]


# Root user
fields = ["first_name", "last_name", "birth_date"]
data = environ["ROOT_DATA"].split(",")

ROOT = {
    "username": environ["ROOT_USERNAME"],
    "email": environ["ROOT_EMAIL"],
    "trader_data": {x: y for x, y in zip(fields, data)},
    "access_level": 1,
    "hashed_password": environ["ROOT_PASS"],
}

# Database
DATABASE_URL = environ["DATABASE_URL"]

# JWT
JWT_SECRET = environ["JWT_SECRET"]
JWT_ALGORITHM = environ["JWT_ALGORITHM"]
ACCESS_TOKEN_EXPIRE_DAYS = environ["ACCESS_TOKEN_EXPIRE_DAYS"]
