from typing import Any

from sqlalchemy import JSON, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Hotel(Base):
    __tablename__ = 'hotels'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)
    services: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    rooms_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    image_id: Mapped[int] = mapped_column(Integer)
    
    rooms = relationship('Room', back_populates='hotel')
    
    def __str__(self) -> str:
        return self.name