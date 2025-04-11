from datetime import datetime, timedelta, UTC
from typing import List, Optional

from fastapi import HTTPException, status
from sqlmodel import Session, select, func, Integer

from app.models.reservation import Reservation
from app.models.table import Table
from app.schemas.reservation import ReservationCreate, ReservationUpdate


class ReservationService:
    """
    Service for managing table reservations.
    """

    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Reservation]:
        """
        Get all reservations.
        
        Returns:
            List[Reservation]: List of all reservations
        """
        statement = select(Reservation)
        return self.session.exec(statement).all()

    def get_by_id(self, reservation_id: int) -> Optional[Reservation]:
        """
        Get reservation by ID.
        
        Args:
            reservation_id: Reservation ID
            
        Returns:
            Optional[Reservation]: Reservation if found, None otherwise
        """
        return self.session.get(Reservation, reservation_id)

    def get_by_table_id(self, table_id: int) -> List[Reservation]:
        """
        Get all reservations for a specific table.
        
        Args:
            table_id: Table ID
            
        Returns:
            List[Reservation]: List of reservations for the table
        """
        statement = select(Reservation).where(Reservation.table_id == table_id)
        return self.session.exec(statement).all()

    def check_time_conflict(
        self,
        table_id: int,
        reservation_time: datetime,
        duration_minutes: int,
        exclude_id: Optional[int] = None
    ) -> bool:
        """
        Check if there is a time conflict for the given table.
        
        Args:
            table_id: Table ID
            reservation_time: Start time of the reservation
            duration_minutes: Duration of the reservation
            exclude_id: Reservation ID to exclude from check (for updates)
            
        Returns:
            bool: True if there is a conflict, False otherwise
        """
        # Ensure reservation_time is timezone-aware
        if reservation_time.tzinfo is None:
            reservation_time = reservation_time.replace(tzinfo=UTC)
            
        end_time = reservation_time + timedelta(minutes=duration_minutes)
        
        # Get all reservations for the table
        reservations = self.session.exec(
            select(Reservation).where(
                Reservation.table_id == table_id,
                Reservation.id != exclude_id if exclude_id else True
            )
        ).all()
        
        # Check for conflicts
        for reservation in reservations:
            # Ensure reservation time is timezone-aware
            res_time = reservation.reservation_time
            if res_time.tzinfo is None:
                res_time = res_time.replace(tzinfo=UTC)
                
            res_end_time = res_time + timedelta(minutes=reservation.duration_minutes)
            
            # Check if there is an overlap
            if (
                (res_time <= reservation_time and reservation_time < res_end_time) or
                (res_time < end_time and end_time <= res_end_time)
            ):
                return True
                
        return False

    def create(self, reservation_data: ReservationCreate) -> Optional[Reservation]:
        """
        Create a new reservation.
        
        Args:
            reservation_data: Reservation data
            
        Returns:
            Optional[Reservation]: Created reservation if successful, None if conflict
            
        Raises:
            HTTPException: If table is not found
        """
        # Check if table exists
        table = self.session.get(Table, reservation_data.table_id)
        if not table:
            return None

        # Check for time conflicts
        if self.check_time_conflict(
            reservation_data.table_id,
            reservation_data.reservation_time,
            reservation_data.duration_minutes
        ):
            return None

        # Create reservation
        reservation = Reservation(**reservation_data.model_dump())
        self.session.add(reservation)
        self.session.commit()
        self.session.refresh(reservation)
        return reservation

    def update(
        self,
        reservation_id: int,
        reservation_data: ReservationUpdate
    ) -> Optional[Reservation]:
        """
        Update an existing reservation.
        
        Args:
            reservation_id: Reservation ID
            reservation_data: Updated reservation data
            
        Returns:
            Optional[Reservation]: Updated reservation if successful, None if not found or conflict
        """
        reservation = self.get_by_id(reservation_id)
        if not reservation:
            return None

        # Get update data
        update_data = reservation_data.model_dump(exclude_unset=True)
        
        # If updating time-related fields, check for conflicts
        if any(key in update_data for key in ['table_id', 'reservation_time', 'duration_minutes']):
            table_id = update_data.get('table_id', reservation.table_id)
            reservation_time = update_data.get('reservation_time', reservation.reservation_time)
            duration_minutes = update_data.get('duration_minutes', reservation.duration_minutes)
            
            if self.check_time_conflict(
                table_id,
                reservation_time,
                duration_minutes,
                exclude_id=reservation_id
            ):
                return None

        # Apply updates
        for key, value in update_data.items():
            setattr(reservation, key, value)

        self.session.add(reservation)
        self.session.commit()
        self.session.refresh(reservation)
        return reservation

    def delete(self, reservation_id: int) -> bool:
        """
        Delete a reservation.
        
        Args:
            reservation_id: Reservation ID
            
        Returns:
            bool: True if reservation was deleted, False otherwise
        """
        reservation = self.get_by_id(reservation_id)
        if not reservation:
            return False

        self.session.delete(reservation)
        self.session.commit()
        return True 