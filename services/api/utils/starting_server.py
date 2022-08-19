# Python
import os

# Database
from database import SessionLocal
from database.queries import get_row, write_row


def check_root(root_user: dict):
    db = SessionLocal()
    root = get_row(db, "Trader", username=root_user["username"])
    if root is None:
        root = write_row(db, "Trader", with_dict=root_user)
        print(f"Superuser created: {root.username}")
    print("Welcome to OTI")
    db.close()


def create_directories(directories: list):
    for dir in directories:
        os.makedirs(dir, exist_ok=True)
