from datetime import datetime

from sqlmodel import Field, Relationship

from app.db.base import BaseModel
from app.models.table import Table


class Reservation(BaseModel, table=True):
    """
    Reservation model representing a table booking.
    """
    __tablename__ = "reservations"

    customer_name: str = Field(index=True)
    table_id: int = Field(foreign_key="tables.id", index=True)
    reservation_time: datetime = Field(index=True)
    duration_minutes: int = Field(ge=1)

    # Relationship
    table: Table = Relationship(back_populates="reservations")

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "customer_name": "John Doe",
                "table_id": 1,
                "reservation_time": "2024-01-01T19:00:00",
                "duration_minutes": 120,
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-01T12:00:00"
            }
        } 