from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.mixins import FundMixin
from app.models.user import User
from app.schemas.base import FundsBase


class FundsManagerBase:
    crud: CRUDBase
    target_crud: CRUDBase

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self):
        return await self.crud.get_all(self._session)

    async def create(self, obj_in: FundsBase, user: Optional[User] = None):
        create_datetime = datetime.now()
        funding_targets = await self.target_crud.get_uninvested(self._session)
        invested_amount = self._allocate_funds(
            obj_in.full_amount,
            funding_targets,
        )
        obj_data = {
            **obj_in.dict(),
            "invested_amount": invested_amount,
            "create_date": create_datetime,
        }
        obj_db = await self.crud.create(obj_data, self._session, user)
        return obj_db

    def _allocate_funds(self, amount: int, targets: list[FundMixin]) -> int:
        amount_to_allocate = amount
        active_targets = []
        for target in targets:
            if amount_to_allocate == 0:
                break
            amount_to_allocate = target.invest(amount_to_allocate)
            active_targets.append(target)
        self._session.add_all(active_targets)
        invested_amount = amount - amount_to_allocate
        return invested_amount
