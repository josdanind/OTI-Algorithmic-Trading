# FastAPI
from fastapi import FastAPI

# Routers
from .routers import api, assets

# Environment Variables
from .config import APP_VERSION, ROOT, DIRECTORIES

# Database
from .database import engine, models

# Utils
from .utils.starting_server import check_root, create_directories


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="OTI Bot", version=APP_VERSION)
app.include_router(api)
app.include_router(assets)


@app.on_event("startup")
def startup():
    check_root(ROOT)
    create_directories(DIRECTORIES)
