from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.models.mixins import FundMixin


class CRUDBase:
    def __init__(self, model) -> None:
        self.model = model

    async def create(
        self,
        data: dict,
        session: AsyncSession,
        user: Optional[User] = None,
    ):
        if user is not None:
            data["user_id"] = user.id
        db_obj = self.model(**data)
        session.add(db_obj)  # type: ignore
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_all(self, session: AsyncSession):
        objects = await session.execute(select(self.model))
        return objects.scalars().all()

    async def get_uninvested(self, session: AsyncSession) -> list[FundMixin]:
        stmt = (
            select(self.model)
            .where(~self.model.fully_invested)
            .order_by(self.model.create_date)
        )
        open_objects = await session.execute(stmt)
        return open_objects.scalars().all()
