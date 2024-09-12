from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.services.funds_base import FundsManagerBase


class DonationManager(FundsManagerBase):
    crud = donation_crud
    target_crud = charity_project_crud

    async def get_user_donations(self, user_id: int):
        return await self.crud.get_user_donations(self._session, user_id)
