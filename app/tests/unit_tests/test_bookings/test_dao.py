from datetime import datetime

from app.bookings.dao import BookingDAO


async def test_add_and_get_booking():
    new_booking = await BookingDAO.add(
        user_id=2,
        room_id=1,
        date_from=datetime.strptime('2023-07-10', "%Y-%m-%d"),
        date_to=datetime.strptime('2023-07-24', "%Y-%m-%d")
    )
    
    assert new_booking.user_id == 2
    assert new_booking.room_id == 1
    
    booking = await BookingDAO.find_by_id(new_booking.id)
    
    assert booking is not None
    
async def test_get_rooms_left():
    rooms_left = await BookingDAO.get_rooms_left(
        1,
        datetime.strptime('2023-05-10', "%Y-%m-%d"),
        datetime.strptime('2023-05-20', "%Y-%m-%d")
    )
    
    assert rooms_left == 5