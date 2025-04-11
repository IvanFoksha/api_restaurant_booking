from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlmodel import Field, SQLModel

from app.models.base import BaseModel
from app.models.enums import ReservationStatus


class Reservation(BaseModel, table=True):
    """
    Reservation model representing a table booking.
    """
    __tablename__ = "reservations"

    customer_name: str = Field(sa_column=Column(String(100)))
    customer_email: str = Field(sa_column=Column(String(100)))
    customer_phone: str = Field(sa_column=Column(String(20)))
    party_size: int = Field()
    reservation_time: datetime = Field()
    status: ReservationStatus = Field(
        sa_column=Column(String(20)),
        default=ReservationStatus.PENDING
    )

    # Foreign key and relationship
    table_id: int = Field(foreign_key="tables.id")
    table: "Table" = Field(
        sa_relationship=relationship("Table", back_populates="reservations")
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "customer_name": "John Doe",
                "customer_email": "john@example.com",
                "customer_phone": "+1234567890",
                "party_size": 4,
                "reservation_time": "2024-01-01T19:00:00",
                "status": "pending",
                "table_id": 1,
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-01T12:00:00"
            }
        } 