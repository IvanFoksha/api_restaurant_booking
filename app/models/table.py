from datetime import datetime
from typing import TYPE_CHECKING, Optional, List

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.models.reservation import Reservation


class Table(SQLModel, table=True):
    """
    Table model representing a restaurant table.
    """
    __tablename__ = "tables"

    id: Optional[int] = Field(default=None, primary_key=True)
    number: int = Field(unique=True, index=True)
    capacity: int
    location: str
    is_available: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    reservations: List["Reservation"] = Relationship(back_populates="table")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "number": 1,
                "capacity": 4,
                "location": "Window",
                "is_available": True,
                "created_at": "2024-04-11T12:00:00",
                "updated_at": "2024-04-11T12:00:00"
            }
        }
