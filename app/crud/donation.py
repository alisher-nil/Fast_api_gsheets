from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation


class CRUDDonation(CRUDBase):
    async def get_user_donations(self, session: AsyncSession, user_id: int):
        stmt = select(Donation).where(Donation.user_id == user_id)
        donations = await session.execute(stmt)
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
