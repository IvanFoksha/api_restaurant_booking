from datetime import datetime, timedelta

import pytest
from sqlmodel import Session

from app.models.table import Table
from app.models.reservation import Reservation


def test_create_table(session: Session):
    table = Table(
        number=1,
        capacity=4,
        location="Window",
        is_available=True
    )
    session.add(table)
    session.commit()
    session.refresh(table)

    assert table.id is not None
    assert table.number == 1
    assert table.capacity == 4
    assert table.location == "Window"
    assert table.is_available is True


def test_create_reservation(session: Session, table: Table):
    reservation = Reservation(
        table_id=table.id,
        guest_name="Test Guest",
        guest_email="test@example.com",
        guest_phone="+1234567890",
        party_size=2,
        reservation_time=datetime.utcnow() + timedelta(days=1),
        duration=120,
        status="pending"
    )
    session.add(reservation)
    session.commit()
    session.refresh(reservation)

    assert reservation.id is not None
    assert reservation.table_id == table.id
    assert reservation.guest_name == "Test Guest"
    assert reservation.guest_email == "test@example.com"
    assert reservation.guest_phone == "+1234567890"
    assert reservation.party_size == 2
    assert reservation.duration == 120
    assert reservation.status == "pending"


def test_table_reservation_relationship(session: Session, table: Table):
    # Create a reservation for the table
    reservation = Reservation(
        table_id=table.id,
        guest_name="Test Guest",
        guest_email="test@example.com",
        guest_phone="+1234567890",
        party_size=2,
        reservation_time=datetime.utcnow() + timedelta(days=1),
        duration=120,
        status="pending"
    )
    session.add(reservation)
    session.commit()
    session.refresh(table)

    # Check relationship
    assert len(table.reservations) == 1
    assert table.reservations[0].id == reservation.id
    assert reservation.table.id == table.id
