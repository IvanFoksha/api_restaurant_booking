from datetime import datetime, UTC
from sqlmodel import Session

from app.models.table import Table
from app.models.reservation import Reservation


def test_create_table(db_session: Session):
    """Test creating a table."""
    table = Table(
        name="Test Table",
        seats=4,
        location="Main Hall"
    )
    db_session.add(table)
    db_session.commit()
    db_session.refresh(table)

    assert table.id is not None
    assert table.name == "Test Table"
    assert table.seats == 4
    assert table.location == "Main Hall"


def test_create_reservation(db_session: Session, table_fixture: Table):
    """Test creating a reservation."""
    reservation = Reservation(
        customer_name="Test Customer",
        reservation_time=datetime.now(UTC),
        duration_minutes=60,
        table_id=table_fixture.id
    )
    db_session.add(reservation)
    db_session.commit()
    db_session.refresh(reservation)

    assert reservation.id is not None
    assert reservation.customer_name == "Test Customer"
    assert reservation.table_id == table_fixture.id


def test_table_reservation_relationship(db_session: Session, table_fixture: Table):
    """Test table-reservation relationship."""
    # Create a reservation
    reservation = Reservation(
        customer_name="Test Customer",
        reservation_time=datetime.now(UTC),
        duration_minutes=60,
        table_id=table_fixture.id
    )
    db_session.add(reservation)
    db_session.commit()
    db_session.refresh(reservation)

    # Test relationship
    assert reservation.table_id == table_fixture.id
    assert table_fixture.reservations[0].id == reservation.id
