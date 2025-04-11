from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    """Base model with common fields."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True

    def __mapper_args__(cls):
        return {
            "concrete": True,  # Указываем, что это конкретное наследование
        } 