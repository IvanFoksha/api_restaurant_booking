import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from app.core.config import settings
from app.main import app
from app.models.table import Table
from app.models.reservation import Reservation


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        yield session

    app.dependency_overrides[settings.get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="table")
def table_fixture(session: Session):
    table = Table(
        number=1,
        capacity=4,
        location="Window",
        is_available=True
    )
    session.add(table)
    session.commit()
    session.refresh(table)
    return table


@pytest.fixture(name="reservation")
def reservation_fixture(session: Session, table: Table):
    from datetime import datetime, timedelta
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
    return reservation
