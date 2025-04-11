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
    guest_name: str
    guest_email: str
    guest_phone: str
    party_size: int
    reservation_time: datetime
    duration: int = Field(default=120)  # Duration in minutes
    status: str = Field(default="pending")
    notes: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    table: "Table" = Relationship(back_populates="reservations")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "table_id": 1,
                "guest_name": "John Doe",
                "guest_email": "john@example.com",
                "guest_phone": "+1234567890",
                "party_size": 2,
                "reservation_time": "2024-04-11T19:00:00",
                "duration": 120,
                "status": "confirmed",
                "notes": "Window seat preferred",
                "created_at": "2024-04-11T12:00:00",
                "updated_at": "2024-04-11T12:00:00"
            }
        }
