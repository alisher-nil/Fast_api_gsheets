from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt

from app.core.constants import STRING_FIELD_MIN_LENGTH
from app.schemas.base import FundsBase


class DonationBase(FundsBase, BaseModel):
    comment: Optional[str]


class DonationDB(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class FullDonationDB(DonationDB):
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
    user_id: int

    class Config:
        orm_mode = True


class DonationCreate(DonationBase):
    full_amount: PositiveInt = Field(...)
    comment: Optional[str] = Field(None, min_length=STRING_FIELD_MIN_LENGTH)
