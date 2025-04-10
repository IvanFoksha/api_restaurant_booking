from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    """
    Base model class that includes common fields for all database models.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"nullable": False}
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"nullable": False}
    )

    class Config:
        arbitrary_types_allowed = True 