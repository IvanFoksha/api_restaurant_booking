from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, Field, validator
from sqlmodel import SQLModel

from app.schemas.table import TableResponse


class ReservationBase(SQLModel):
    """
    Base schema for reservation data.
    """
    customer_name: str
    reservation_time: datetime
    duration_minutes: int = Field(default=60)
    table_id: int


class ReservationCreate(ReservationBase):
    """
    Schema for creating a new reservation.
    """
    @validator("reservation_time")
    def validate_future_time(cls, v):
        """
        Validate that reservation time is in the future.
        """
        now = datetime.now(v.tzinfo if v.tzinfo else None)
        if v < now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reservation time must be in the future"
            )
        return v


class ReservationUpdate(SQLModel):
    """
    Schema for updating an existing reservation.
    """
    customer_name: Optional[str] = None
    reservation_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    table_id: Optional[int] = None

    @validator("reservation_time")
    def validate_future_time(cls, v):
        """
        Validate that reservation time is in the future.
        """
        if v is not None:
            now = datetime.now(v.tzinfo if v.tzinfo else None)
            if v < now:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Reservation time must be in the future"
                )
        return v


class ReservationRead(ReservationBase):
    """
    Schema for reading reservation data.
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


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
