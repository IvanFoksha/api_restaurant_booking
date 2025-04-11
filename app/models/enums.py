from enum import Enum


class ReservationStatus(str, Enum):
    """Enum for reservation status."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled" 