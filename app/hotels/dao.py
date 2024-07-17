from sqlalchemy import and_, func, insert, or_, select

from app.bookings.dao import BookingDAO
from app.bookings.models import Booking
from app.dao.base import BaseDAO
from app.db import async_session, engine
from app.rooms.dao import RoomDAO
from app.rooms.models import Room

from .models import Hotel


class HotelDAO(BaseDAO):
    model = Hotel

    @classmethod
    async def get_hotel(cls, location, date_from, date_to):
        hotels = select(cls.model).where(cls.model.location.like(f"%{location}%"))
        
        async with async_session() as session:
            hotels = await session.scalars(hotels)
            hotels_data = hotels.all()
            data = []
            for hotel in hotels_data:
                hotel_rooms_left = 0
                rooms = await RoomDAO.find_all(hotel_id=hotel.id)
                for room in rooms:
                    rooms_left = await BookingDAO.get_rooms_left(room['id'], date_from, date_to)
                    hotel_rooms_left += rooms_left
                hotel.__dict__['rooms_left'] = hotel_rooms_left
                if hotel_rooms_left > 0:
                    data.append(hotel)
            return data
