from datetime import datetime
from typing import Any

from sqlalchemy import (JSON, Computed, DateTime, ForeignKey, Integer,
                        Interval, String)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Booking(Base):
    __tablename__ = 'bookings'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    room_id: Mapped[int] = mapped_column(Integer, ForeignKey('rooms.id'))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    date_from: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    date_to: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    total_cost: Mapped[int] = mapped_column(Integer, Computed("DATE_PART('day', (date_to - date_from)) * price::int"))
    total_days: Mapped[int] = mapped_column(Integer, Computed("DATE_PART('day', (date_to - date_from))::int"))
    
    user = relationship('User', back_populates='bookings')
    room = relationship('Room', back_populates='bookings')
    
    def __str__(self) -> str:
        return f"Booking #{self.id}"