from fastapi import HTTPException

from app.core.constants import MIN_INVESTMENT_THRESHOLD
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.services.funds_base import FundsManagerBase


class CharityProjectManager(FundsManagerBase):
    crud = charity_project_crud
    target_crud = donation_crud

    async def get(self, project_id: int):
        return await self.crud.get(project_id, self._session)

    async def create(self, project_in: CharityProjectCreate):
        await self._validate_name(project_in.name)
        return await super().create(project_in)

    async def delete(self, project_id: int):
        project = await self.get_project_or_404(project_id)
        self._check_project_can_be_deleted(project)
        project = await self.crud.remove(project, self._session)
        return project

    async def update(self, project_id: int, project_in: CharityProjectUpdate):
        project = await self.get_project_or_404(project_id)
        self._check_project_can_be_edited(project)
        await self._validate_update_data(project, project_in)
        update_data = project_in.dict(exclude_unset=True)
        project = await self.crud.update(project, update_data, self._session)
        return project

    async def get_project_or_404(self, project_id: int) -> CharityProject:
        project = await self.get(project_id)
        if project is None:
            raise HTTPException(
                status_code=404,
                detail="Charity project not found",
            )
        return project

    async def _validate_update_data(
        self,
        project: CharityProject,
        data: CharityProjectUpdate,
    ):
        if data.name is not None:
            await self._validate_name(data.name)
        if data.full_amount is not None:
            self._check_new_full_amount(project, data.full_amount)

    def _check_new_full_amount(self, project: CharityProject, amount: int):
        if amount < project.invested_amount:
            raise HTTPException(
                status_code=400,
                detail="Cannot set new amount lower than invested amount.",
            )

    def _check_project_can_be_deleted(self, project: CharityProject):
        if project.invested_amount > MIN_INVESTMENT_THRESHOLD:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete invested project.",
            )

    def _check_project_can_be_edited(self, project: CharityProject):
        if project.fully_invested:
            raise HTTPException(
                status_code=400,
                detail="Cannot edit closed projects.",
            )

    async def _validate_name(self, name: str):
        project = await self.crud.get_project_by_name(name, self._session)
        if project is not None:
            raise HTTPException(
                status_code=400,
                detail="A project with this name already exists.",
            )
