from datetime import date

from fastapi import APIRouter, Depends, Request
from fastapi_cache.decorator import cache
from fastapi_versioning import version

from app.exceptions import RoomCanNotBeBooked
from app.users.dependencies import get_current_user
from app.users.models import User

from .dao import HotelDAO


router = APIRouter(
    prefix='/hotels',
    tags=['Hotels']
)

@router.get("{location}")
@cache(expire=60)
@version(1)
async def get_hotels_by_location(
    location: str,
    date_from: date,
    date_to: date
    ):
    result = await HotelDAO.get_hotel(location, date_from, date_to)
    return result