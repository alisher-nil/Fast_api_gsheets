from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer


class FundMixin:
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False, default=0)
    fully_invested = Column(Boolean, nullable=False, default=False)
    create_date = Column(DateTime, nullable=False, default=datetime.now)
    close_date = Column(DateTime)

    @property
    def remaining_amount(self) -> int:
        return self.full_amount - self.invested_amount

    def invest(self, amount: int) -> int:
        """
        Allocate funds and return the amount that could not be allocated.
        """
        result = self.invested_amount + amount
        if result >= self.full_amount:
            self.invested_amount = self.full_amount
            return result - self.full_amount
        else:
            self.invested_amount = result
            return 0

    def close(self) -> None:
        """
        Close the fund by marking it as fully invested
        and setting the close date.
        """
        self.fully_invested = True
        self.close_date = datetime.now()
