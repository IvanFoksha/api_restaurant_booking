from datetime import datetime, timedelta, UTC

from fastapi.testclient import TestClient

from app.models.table import Table
from app.models.reservation import Reservation


def test_create_table(client: TestClient):
    """Test creating a table."""
    response = client.post(
        "/api/v1/tables/",
        json={
            "name": "Table 1",
            "seats": 4,
            "location": "Main Hall"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Table 1"
    assert data["seats"] == 4
    assert data["location"] == "Main Hall"
    return data["id"]


def test_get_tables(client: TestClient, table_fixture: Table):
    """Test getting all tables."""
    response = client.get("/api/v1/tables/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == table_fixture.name


def test_create_reservation(client: TestClient, table_fixture: Table):
    """Test creating a reservation."""
    response = client.post(
        "/api/v1/reservations/",
        json={
            "customer_name": "Test Customer",
            "table_id": table_fixture.id,
            "reservation_time": (datetime.now(UTC) + timedelta(days=1)).isoformat(),
            "duration_minutes": 60
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == "Test Customer"
    assert data["table_id"] == table_fixture.id
    return data["id"]


def test_get_reservations(client: TestClient, table_fixture: Table):
    """Test getting all reservations."""
    # First create a reservation
    test_create_reservation(client, table_fixture)
    
    # Then get all reservations
    response = client.get("/api/v1/reservations/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["table_id"] == table_fixture.id


def test_reservation_conflict(client: TestClient, table_fixture: Table):
    """Test reservation time conflict."""
    # Create first reservation
    first_reservation = {
        "customer_name": "First Customer",
        "table_id": table_fixture.id,
        "reservation_time": (datetime.now(UTC) + timedelta(days=1)).isoformat(),
        "duration_minutes": 60
    }
    client.post("/api/v1/reservations/", json=first_reservation)

    # Try to create overlapping reservation
    second_reservation = {
        "customer_name": "Second Customer",
        "table_id": table_fixture.id,
        "reservation_time": (
            datetime.fromisoformat(first_reservation["reservation_time"]) +
            timedelta(minutes=30)
        ).isoformat(),
        "duration_minutes": 60
    }
    response = client.post("/api/v1/reservations/", json=second_reservation)
    assert response.status_code == 400
