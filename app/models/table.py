from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlmodel import SQLModel

from app.db.base import BaseModel
from app.models.reservation import Reservation


class Table(SQLModel, table=True):
    """
    Table model representing a restaurant table.
    """
    __tablename__ = "tables"

    id: Optional[int] = Column(Integer, primary_key=True, index=True)
    number: int = Column(Integer, unique=True, index=True)
    capacity: int
    location: str = Column(String(100))
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Use string reference for relationship
    reservations: List["Reservation"] = relationship(
        "Reservation",
        back_populates="table",
        cascade="all, delete-orphan"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "number": 1,
                "capacity": 4,
                "location": "Main Hall",
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-01T12:00:00"
            }
        }
