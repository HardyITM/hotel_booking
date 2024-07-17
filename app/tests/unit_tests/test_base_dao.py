from contextlib import nullcontext

import pytest
from sqlalchemy.exc import IntegrityError

from app.hotels.dao import HotelDAO
from app.rooms.dao import RoomDAO
from app.users.dao import UsersDAO


@pytest.mark.parametrize(
    "id,exists",
    [
        (1, True),
        (2, True),
        (3, False)
    ]
)
async def test_find_user_by_id(id, exists):
    user = await UsersDAO.find_by_id(id)
    if exists:
        assert user
        assert user.id == id
    else:
        assert not user


@pytest.mark.parametrize(
    'id,exists',
    [
        (1, True),
        (5, True),
        (7, False)
    ]
)
async def test_find_one_or_none_hotel(id, exists):
    hotel = await HotelDAO.find_one_or_none(id=id)
    if exists:
        assert hotel
        assert hotel.id == id
    else:
        assert not hotel


@pytest.mark.parametrize(
    'id,count',
    [
        (1, 2),
        (5, 2),
        (6, 1),
    ]
)
async def test_find_all_rooms(id, count):
    rooms = await RoomDAO.find_all(hotel_id=id)
    assert len(rooms) == count


@pytest.mark.parametrize(
    'name,location,services,rooms_quantity,image_id,expectation',
    [
        ('Test', 'Loc test', ['Test serv', 'Test serv2'], 5, 10, nullcontext()),
        ('Test', 'Loc test', ['Test serv', 'Test serv2'], 5, None, pytest.raises(IntegrityError))
    ]
)
async def test_add_data_hotel(
    name,
    location,
    services,
    rooms_quantity,
    image_id,
    expectation
    ):
    with expectation:
        hotel = await HotelDAO.add_data(
            name=name,
            location=location,
            services=services,
            rooms_quantity=rooms_quantity,
            image_id=image_id
        )
        test_hotel = await HotelDAO.find_by_id(hotel)
        assert test_hotel
        assert test_hotel.name == 'Test'
