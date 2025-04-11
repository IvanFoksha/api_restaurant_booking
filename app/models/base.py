from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Integer
from sqlmodel import SQLModel


class BaseModel(SQLModel):
    """Base model with common fields."""
    id: Optional[int] = Column(Integer, primary_key=True, index=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    ) 