from config import DATABASE_URL

# sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Cotrol de sesiones
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
