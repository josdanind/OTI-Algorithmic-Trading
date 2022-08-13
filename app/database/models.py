# Python
from datetime import datetime

# Utils
from ..utils.encrypt_password import context

# SQLAlchemy
from sqlalchemy_json import MutableJson
from . import Base
from sqlalchemy import (
    Column,
    ForeignKey,
    Identity,
    Integer,
    String,
    DateTime,
    Float,
    Boolean,
)


class Trader(Base):
    __tablename__ = "traders"

    username = Column(String(50), primary_key=True, unique=True, nullable=False)
    id = Column(Integer, Identity(start=1, cycle=True))
    access_level = Column(Integer, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    trader_data = Column(MutableJson, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime)

    def set_password(self, password):
        self.hashed_password = context.hash(password)
