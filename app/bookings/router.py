from datetime import date

from fastapi import APIRouter, Depends
from pydantic import TypeAdapter
from fastapi_versioning import version

from app.exceptions import BookingNotFound, RoomCanNotBeBooked
from app.tasks.tasks import send_booking_confirmation
from app.users.dependencies import get_current_user
from app.users.models import User

from .dao import BookingDAO
from .schemas import SBooking

router = APIRouter(
    prefix='/bookings',
    tags=['Bookings']
)

@router.get("")
@version(1)
async def get_bookings(
    user: User = Depends(get_current_user)
    ) -> list[SBooking]:
    result = await BookingDAO.find_all(user_id=user.id)
    return result

@router.get("/{booking_id}")
@version(1)
async def get_booking(booking_id: int) -> SBooking:
    result = await BookingDAO.find_by_id(booking_id)
    if not result:
        raise BookingNotFound
    return result

@router.post("")
@version(1)
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: User = Depends(get_current_user)
    ):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCanNotBeBooked
    BookingAdapter = TypeAdapter(SBooking)
    booking_dict = BookingAdapter.validate_python(booking, from_attributes=True).model_dump()
    send_booking_confirmation.delay(booking_dict, user.email)
    return booking_dict['id']