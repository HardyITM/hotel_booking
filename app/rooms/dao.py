from sqlalchemy import and_, func, insert, or_, select

from app.bookings.dao import BookingDAO
from app.bookings.models import Booking
from app.dao.base import BaseDAO
from app.db import async_session, engine

from .models import Room


class RoomDAO(BaseDAO):
    model = Room