from sqlalchemy import and_, func, insert, or_, select
from sqlalchemy.exc import SQLAlchemyError

from app.dao.base import BaseDAO
from app.db import async_session, engine
from app.rooms.models import Room
from app.logger import logger

from .models import Booking


class BookingDAO(BaseDAO):
    model = Booking
    
    @classmethod
    async def get_rooms_left(cls, room_id, date_from, date_to):
        booked_stmt = select(Booking).where(
            and_(
                Booking.room_id == room_id,
                or_(
                    and_(
                    Booking.date_from >= date_from,
                    Booking.date_from <= date_to
                    ),
                    and_(
                    Booking.date_from <= date_from,
                    Booking.date_to > date_from
                    ),
                )
            )
        ).cte('booked_stmt')
        rooms_stmt = select(
            (Room.quantity - func.count(booked_stmt.c.room_id)).label("rooms_stmt")
            ).select_from(Room).join(
                booked_stmt, booked_stmt.c.room_id == Room.id, isouter=True
            ).where(Room.id == room_id).group_by(
                Room.quantity, booked_stmt.c.room_id
            )
            
        async with async_session() as session:
            rooms_left = await session.scalar(rooms_stmt)
            return rooms_left
    
    @classmethod
    async def add(cls, user_id, room_id, date_from, date_to):
        try:
            async with async_session() as session:
                rooms_left = await cls.get_rooms_left(room_id, date_from, date_to)
                if rooms_left is not None and rooms_left > 0:
                    get_price_stmt = select(Room.price).filter_by(id=room_id)
                    price = await session.scalar(get_price_stmt)
                    add_booking_stmt = insert(Booking).values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price
                    ).returning(Booking)
                    result = await session.execute(add_booking_stmt)
                    await session.commit()
                    return result.scalar()
                else:
                    return None
        except (SQLAlchemyError, Exception) as err:
            if isinstance(err, SQLAlchemyError):
                msg = "Database Exc"
            elif isinstance(err, Exception):
                msg = "Unknown Exc"
            msg += ": Cannot add booking"
            extra = {
                "user_id": user_id,
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to
            }
            logger.error(
                msg,
                extra=extra,
                exc_info=True   
            )