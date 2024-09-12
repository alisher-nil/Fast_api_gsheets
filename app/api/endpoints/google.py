from fastapi import APIRouter, Depends

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import CharityProjectDB
from app.services.google_api import create_report

router = APIRouter()


@router.get(
    "/closed",
    response_model=list[CharityProjectDB],
    dependencies=[Depends(current_superuser)],
)
async def get_closed_project(
    session=Depends(get_async_session),
    service=Depends(get_service),
):
    """
    Только для суперюзеров.

    Возвращает список проектов, отсортированных по скорости закрытия и
    создает таблицу в google sheets с отчетом по проектам.
    """
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    await create_report(projects, service)
    return projects
