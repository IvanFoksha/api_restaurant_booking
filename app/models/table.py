from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlmodel import Field, SQLModel

from app.models.base import BaseModel
from app.models.reservation import Reservation


class Table(BaseModel, table=True):
    """
    Table model representing a restaurant table.
    """
    __tablename__ = "tables"

    number: int = Field(sa_column=Column(Integer, unique=True, index=True))
    capacity: int = Field()
    location: str = Field(sa_column=Column(String(100)))

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
