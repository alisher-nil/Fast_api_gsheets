from fastapi import FastAPI

from app.api.routers import main_router
from app.core.init_db import create_first_superuser

app = FastAPI(
    title="Кошачий благотворительный фонд",
    description="Сервис для поддержки котиков!",
    version="0.1.0",
)
app.include_router(main_router)


@app.on_event("startup")
async def startup_event():
    await create_first_superuser()
