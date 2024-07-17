from typing import Any

from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Room(Base):
    __tablename__ = 'rooms'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hotel_id: Mapped[int] = mapped_column(Integer, ForeignKey('hotels.id'))
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    services: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    image_id: Mapped[int] = mapped_column(Integer)
    
    hotel = relationship('Hotel', back_populates='rooms')
    bookings = relationship('Booking', back_populates='room')
    
    def __str__(self) -> str:
        return self.name