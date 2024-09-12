# type: ignore
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get(self, id: int, session: AsyncSession):
        charity_project = await session.get(CharityProject, id)
        return charity_project

    async def remove(
        self,
        charity_project: CharityProject,
        session: AsyncSession,
    ):
        await session.delete(charity_project)
        await session.commit()
        return charity_project

    async def update(
        self,
        charity_project: CharityProject,
        update_data: dict,
        session: AsyncSession,
    ):
        project_data = jsonable_encoder(charity_project)
        for field in project_data:
            if field in update_data:
                setattr(charity_project, field, update_data[field])

        session.add(charity_project)
        await session.commit()
        await session.refresh(charity_project)
        return charity_project

    async def get_project_by_name(
        self,
        name: str,
        session: AsyncSession,
    ) -> Optional[CharityProject]:
        project = await session.execute(
            select(CharityProject).where(CharityProject.name == name)
        )
        project = project.scalars().first()
        return project

    async def get_projects_by_completion_rate(self, session: AsyncSession):
        # fmt: off
        difference_stmt = (func.julianday(CharityProject.close_date) -
                           func.julianday(CharityProject.create_date))
        # fmt: on
        stmt = (
            select(CharityProject)
            .where(CharityProject.fully_invested)
            .order_by(difference_stmt)
        )
        result = await session.execute(stmt)
        return result.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
