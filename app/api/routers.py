from fastapi import APIRouter

from app.api.endpoints import (
    charity_projects_router,
    donations_router,
    google_router,
    users_router,
)

main_router = APIRouter()
main_router.include_router(
    charity_projects_router,
    tags=["charity_projects"],
    prefix="/charity_project",
)
main_router.include_router(
    donations_router,
    tags=["donations"],
    prefix="/donation",
)
main_router.include_router(
    google_router,
    tags=["google"],
    prefix="/google",
)
main_router.include_router(
    users_router,
    tags=["auth"],
)
