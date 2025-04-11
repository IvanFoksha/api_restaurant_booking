from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Integer
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    """Base model with common fields."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        sa_column=Column(DateTime, default=datetime.utcnow)
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow
        )
    ) 