from datetime import datetime, timedelta

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models import CharityProject

FORMAT = "%Y/%m/%d %H:%M:%S"


async def create_report(
    projects: list[CharityProject],
    wrapper_services: Aiogoogle,
) -> None:
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(spreadsheetid, projects, wrapper_services)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover("sheets", "v4")
    spreadsheet_body = {
        "properties": {
            "title": f"QRKot отчет от {now_date_time}",
            "locale": "ru_RU",
        },
        "sheets": [
            {
                "properties": {
                    "sheetType": "GRID",
                    "sheetId": 0,
                    "title": "Лист1",
                    "gridProperties": {"rowCount": 100, "columnCount": 10},
                }
            }
        ],
    }
    request = service.spreadsheets.create(json=spreadsheet_body)
    response = await wrapper_services.as_service_account(request)
    spreadsheetid = response["spreadsheetId"]
    return spreadsheetid


async def set_user_permissions(
    spreadsheetid: str,
    wrapper_services: Aiogoogle,
) -> None:
    permissions_body = {
        "type": "user",
        "role": "writer",
        "emailAddress": settings.email,
    }
    service = await wrapper_services.discover("drive", "v3")
    request = service.permissions.create(
        fileId=spreadsheetid,
        json=permissions_body,
        fields="id",
    )
    await wrapper_services.as_service_account(request)


async def spreadsheets_update_value(
    spreadsheetid: str,
    projects: list[CharityProject],
    wrapper_services: Aiogoogle,
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover("sheets", "v4")

    table_values = [
        ["Отчёт от", now_date_time],
        ["Топ проектов по скорости закрытия"],
        ["Название проекта", "Время сбора", "Описание"],
    ]
    for project in projects:
        if project.close_date < project.create_date:
            # if the remaining funds were sufficient to close the project
            # at the moment of creation closing time might be
            # earlier than creation time since funds distribution
            # happens prior to db update
            completion_time = timedelta(seconds=0)
        else:
            completion_time = project.close_date - project.create_date
        new_row = [
            project.name,
            str(completion_time),
            project.description,
        ]
        table_values.append(new_row)

    update_body = {"majorDimension": "ROWS", "values": table_values}
    request = service.spreadsheets.values.update(
        spreadsheetId=spreadsheetid,
        range="A1:E30",
        valueInputOption="USER_ENTERED",
        json=update_body,
    )
    await wrapper_services.as_service_account(request)
