from sqlalchemy import insert, select

from app.bookings.models import Booking
from app.db import async_session


class BaseDAO:
    model = None
    
    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session() as session:
            stmt = select(cls.model.__table__.columns).filter_by(id=model_id)
            result = await session.execute(stmt)
            return result.mappings().one_or_none()
    
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session() as session:
            stmt = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(stmt)
            return result.mappings().one_or_none()
    
    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session() as session:
            stmt = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(stmt)
            return result.mappings().all()

    @classmethod
    async def add_data(cls, **data):
        async with async_session() as session:
            stmt = insert(cls.model).values(**data)
            result = await session.execute(stmt)
            pk = result.inserted_primary_key
            await session.commit()
            return pk[0]
