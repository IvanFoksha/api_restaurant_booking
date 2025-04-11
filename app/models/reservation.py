from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlmodel import SQLModel


class Reservation(SQLModel, table=True):
    """
    Reservation model representing a table booking.
    """
    __tablename__ = "reservations"

    id: Optional[int] = Column(Integer, primary_key=True, index=True)
    customer_name: str = Column(String(100))
    customer_email: str = Column(String(100))
    customer_phone: str = Column(String(20))
    party_size: int
    reservation_time: datetime
    status: str = Column(String(20), default="pending")
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign key and relationship
    table_id: int = Column(Integer, ForeignKey("tables.id"))
    table: "Table" = relationship("Table", back_populates="reservations")

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