# Pydantic
from pydantic import BaseModel, Field, EmailStr
from .base_schema import OrmActive, PersonalInformation


class TraderBase(OrmActive, BaseModel):
    username: str = Field(min_length=2, max_length=50)
    access_level: int = Field(default=2)
    email: EmailStr
    trader_data: PersonalInformation


class TraderInDB(TraderBase):
    password: str = Field(min_length=8, max_length=50)


class TraderOut(TraderBase):
    id: int


class TraderResponse(TraderOut):
    message: str | None = None


class TraderUpdate(BaseModel):
    username: str | None = None
    access_level: int | None = None
    email: str | None = None
    password: str | None = None
    # trader_data
    first_name: str | None = None
    last_name: str | None = None
    birth_date: str | None = None
