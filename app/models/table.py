from typing import List

from sqlmodel import Field, Relationship

from app.db.base import BaseModel
from app.models.reservation import Reservation


class Table(BaseModel, table=True):
    """
    Table model representing a restaurant table.
    """
    __tablename__ = "tables"

    name: str = Field(index=True)
    seats: int = Field(ge=1)
    location: str = Field(index=True)

    # Relationship
    reservations: List["Reservation"] = Relationship(back_populates="table")

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Table 1",
                "seats": 4,
                "location": "Main Hall",
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-01T12:00:00"
            }
        }
