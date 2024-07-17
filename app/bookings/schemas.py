import datetime

from pydantic import BaseModel


class SBooking(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: datetime.date
    date_to: datetime.date
    price: int
    total_cost: int
    total_days: int