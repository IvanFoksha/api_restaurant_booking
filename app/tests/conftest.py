from datetime import datetime, UTC
from typing import Generator, Dict, Any
import pytest
from sqlmodel import Session, SQLModel, create_engine
from fastapi.testclient import TestClient

from app.main import app
from app.models.table import Table
from app.models.reservation import Reservation
from app.db.session import get_session


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(
        "sqlite:///./test.db",
        connect_args={"check_same_thread": False}
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def db_session(db_engine) -> Generator[Session, None, None]:
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session) -> Generator[TestClient, None, None]:
    def override_get_session():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def table_fixture(db_session: Session) -> Dict[str, Any]:
    table = Table(
        number=1,
        capacity=4,
        is_available=True
    )
    db_session.add(table)
    db_session.commit()
    db_session.refresh(table)
    return {"id": table.id, "number": table.number}


@pytest.fixture
def reservation_fixture(
    db_session: Session,
    table_fixture: Dict[str, Any]
) -> Dict[str, Any]:
    reservation = Reservation(
        customer_name="Test Customer",
        customer_email="test@example.com",
        party_size=2,
        reservation_time=datetime.now(UTC),
        table_id=table_fixture["id"]
    )
    db_session.add(reservation)
    db_session.commit()
    db_session.refresh(reservation)
    return {"id": reservation.id, "table_id": reservation.table_id}
