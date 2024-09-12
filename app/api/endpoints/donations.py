from fastapi import APIRouter, Depends

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.models import Donation
from app.schemas.donation import DonationCreate, DonationDB, FullDonationDB
from app.services.donation import DonationManager

router = APIRouter()


@router.post("/", response_model=DonationDB, response_model_exclude_none=True)
async def create_donation(
    donation_in: DonationCreate,
    session=Depends(get_async_session),
    user=Depends(current_user),
) -> Donation:
    """Сделать пожертвование."""
    return await DonationManager(session).create(donation_in, user)


@router.get(
    "/",
    response_model=list[FullDonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(session=Depends(get_async_session)):
    """
    Только для суперюзеров.

    Возвращает список всех пожертвований.
    """
    return await DonationManager(session).get_all()


@router.get("/my", response_model=list[DonationDB])
async def get_user_donations(
    session=Depends(get_async_session),
    user=Depends(current_user),
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""
    return await DonationManager(session).get_user_donations(user.id)
