from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TableBase(BaseModel):
    """
    Base schema for Table with common attributes.
    """
    name: str = Field(..., min_length=1, max_length=100)
    seats: int = Field(..., ge=1)
    location: str = Field(..., min_length=1, max_length=100)


class TableCreate(TableBase):
    """
    Schema for creating a new table.
    """
    pass


class TableUpdate(TableBase):
    """
    Schema for updating an existing table.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    seats: Optional[int] = Field(None, ge=1)
    location: Optional[str] = Field(None, min_length=1, max_length=100)


class TableResponse(TableBase):
    """
    Schema for table response.
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
