from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.reservation import (
    ReservationCreate,
    ReservationResponse,
    ReservationUpdate
)
from app.services.reservation import ReservationService

router = APIRouter()


@router.get("/", response_model=List[ReservationResponse])
def get_reservations(
    session: Session = Depends(get_session)
) -> List[ReservationResponse]:
    """
    Get all reservations.
    """
    service = ReservationService(session)
    return service.get_all()


@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
def create_reservation(
    reservation_data: ReservationCreate,
    session: Session = Depends(get_session)
) -> ReservationResponse:
    """
    Create a new reservation.
    """
    service = ReservationService(session)
    reservation = service.create(reservation_data)
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create reservation. Table might not exist or time slot is already booked."
        )
    return reservation


@router.get("/{reservation_id}", response_model=ReservationResponse)
def get_reservation(
    reservation_id: int,
    session: Session = Depends(get_session)
) -> ReservationResponse:
    """
    Get reservation by ID.
    """
    service = ReservationService(session)
    reservation = service.get_by_id(reservation_id)
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reservation with ID {reservation_id} not found"
        )
    return reservation


@router.get("/table/{table_id}", response_model=List[ReservationResponse])
def get_table_reservations(
    table_id: int,
    session: Session = Depends(get_session)
) -> List[ReservationResponse]:
    """
    Get all reservations for a specific table.
    """
    service = ReservationService(session)
    return service.get_by_table_id(table_id)


@router.put("/{reservation_id}", response_model=ReservationResponse)
def update_reservation(
    reservation_id: int,
    reservation_data: ReservationUpdate,
    session: Session = Depends(get_session)
) -> ReservationResponse:
    """
    Update an existing reservation.
    """
    service = ReservationService(session)
    reservation = service.update(reservation_id, reservation_data)
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Reservation with ID {reservation_id} not found or "
                "time slot is already booked"
            )
        )
    return reservation


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(
    reservation_id: int,
    session: Session = Depends(get_session)
) -> None:
    """
    Delete a reservation.
    """
    service = ReservationService(session)
    if not service.delete(reservation_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reservation with ID {reservation_id} not found"
        ) 