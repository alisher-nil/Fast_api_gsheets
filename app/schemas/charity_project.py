from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt

from app.core.constants import (
    PROJECT_NAME_MAX_LENGTH,
    STRING_FIELD_MIN_LENGTH,
)
from app.schemas.base import FundsBase


class CharityProjectBase(FundsBase, BaseModel):
    name: str
    description: str


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ...,
        min_length=STRING_FIELD_MIN_LENGTH,
        max_length=PROJECT_NAME_MAX_LENGTH,
    )
    description: str = Field(
        ...,
        min_length=STRING_FIELD_MIN_LENGTH,
    )
    full_amount: PositiveInt = Field(...)


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(
        None,
        min_length=STRING_FIELD_MIN_LENGTH,
        max_length=PROJECT_NAME_MAX_LENGTH,
    )
    description: Optional[str] = Field(
        None,
        min_length=STRING_FIELD_MIN_LENGTH,
    )
    full_amount: Optional[PositiveInt] = Field(None)
