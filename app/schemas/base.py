from pydantic import BaseModel, Extra, PositiveInt


class FundsBase(BaseModel):
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid
