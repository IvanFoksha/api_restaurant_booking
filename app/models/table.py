from datetime import datetime
from typing import TYPE_CHECKING, Optional, List

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.models.reservation import Reservation


class Table(SQLModel, table=True):
    """
    Table model representing a restaurant table.
    """
    __tablename__ = "tables"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    seats: int
    location: Optional[str] = Field(default="Main Hall")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    reservations: List["Reservation"] = Relationship(back_populates="table")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Table 1",
                "seats": 4,
                "location": "зал у окна",
                "created_at": "2024-04-11T12:00:00",
                "updated_at": "2024-04-11T12:00:00"
            }
        }
