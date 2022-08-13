# FastAPI
from fastapi import FastAPI

# Routers
from .routers import api, assets

# Environment Variables
from .config import APP_VERSION, ROOT

# Database
from .database import engine, models, SessionLocal
from .database.queries import get_row, write_row


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="OTI Bot", version=APP_VERSION)
app.include_router(api)
app.include_router(assets)


@app.on_event("startup")
def startup():
    db = SessionLocal()
    root = get_row(db, "Trader", username=ROOT["username"])
    if root is None:
        root = write_row(db, "Trader", with_dict=ROOT)
        print(f"Superuser created: {root.username}")
    print("Welcome to OTI")
    db.close()
