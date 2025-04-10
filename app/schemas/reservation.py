from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator

from app.schemas.table import TableResponse


class ReservationBase(BaseModel):
    """
    Base schema for Reservation with common attributes.
    """
    customer_name: str = Field(..., min_length=1, max_length=100)
    table_id: int = Field(..., gt=0)
    reservation_time: datetime
    duration_minutes: int = Field(..., ge=1, le=480)  # Max 8 hours


class ReservationCreate(ReservationBase):
    """
    Schema for creating a new reservation.
    """
    @validator("reservation_time")
    def validate_future_time(cls, v):
        """
        Validate that reservation time is in the future.
        """
        if v < datetime.now():
            raise ValueError("Reservation time must be in the future")
        return v


class ReservationUpdate(ReservationBase):
    """
    Schema for updating an existing reservation.
    """
    customer_name: Optional[str] = Field(None, min_length=1, max_length=100)
    table_id: Optional[int] = Field(None, gt=0)
    reservation_time: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, ge=1, le=480)

    @validator("reservation_time")
    def validate_future_time(cls, v):
        """
        Validate that reservation time is in the future.
        """
        if v is not None and v < datetime.now():
            raise ValueError("Reservation time must be in the future")
        return v


class ReservationResponse(ReservationBase):
    """
    Schema for reservation response.
    """
    id: int
    created_at: datetime
    updated_at: datetime
    table: TableResponse

    class Config:
        from_attributes = True
