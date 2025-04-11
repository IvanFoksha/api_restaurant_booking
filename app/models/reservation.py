from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.models.table import Table


class Reservation(SQLModel, table=True):
    """
    Reservation model representing a table booking.
    """
    __tablename__ = "reservations"

    id: Optional[int] = Field(default=None, primary_key=True)
    table_id: int = Field(foreign_key="tables.id")
    customer_name: str
    reservation_time: datetime
    duration_minutes: int = Field(default=60)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    table: "Table" = Relationship(back_populates="reservations")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "table_id": 1,
                "customer_name": "John Doe",
                "reservation_time": "2024-04-11T19:00:00",
                "duration_minutes": 60,
                "created_at": "2024-04-11T12:00:00",
                "updated_at": "2024-04-11T12:00:00"
            }
        }
