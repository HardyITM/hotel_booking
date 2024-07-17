import asyncio
import json
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import insert

from app.bookings.models import Booking
from app.config import settings as s
from app.db import Base, async_session, engine
from app.hotels.models import Hotel
from app.rooms.models import Room
from app.users.models import User
from main import app


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    assert s.MODE == 'TEST'
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding='utf-8') as file:
            return json.load(file)
        
    hotels = open_mock_json('hotels')
    users = open_mock_json('users')
    rooms = open_mock_json('rooms')
    bookings = open_mock_json('bookings')
    
    for booking in bookings:
        booking['date_from'] = datetime.strptime(booking['date_from'], "%Y-%m-%d")
        booking['date_to'] = datetime.strptime(booking['date_to'], "%Y-%m-%d")
    
    async with async_session() as session:
        add_hotels = insert(Hotel).values(hotels)
        add_users = insert(User).values(users)
        add_rooms = insert(Room).values(rooms)
        add_bookings = insert(Booking).values(bookings)
        
        await session.execute(add_hotels)
        await session.execute(add_users)
        await session.execute(add_rooms)
        await session.execute(add_bookings)
        
        await session.commit()
        
# @pytest.fixture(scope='session')
# def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()
    
@pytest.fixture(scope='function')
async def ac():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
        
@pytest.fixture(scope='function')
async def session():
    async with async_session() as session:
        yield session