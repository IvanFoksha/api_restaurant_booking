from datetime import datetime, timedelta, UTC
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.table import Table
from app.models.reservation import Reservation


def test_create_reservation(client: TestClient, table_fixture: Table):
    """Test creating a new reservation."""
    # Create reservation time 1 hour from now
    reservation_time = (
        datetime.now(table_fixture.created_at.tzinfo) + timedelta(hours=1)
    )
    response = client.post(
        "/api/v1/reservations/",
        json={
            "customer_name": "John Doe",
            "table_id": table_fixture.id,
            "reservation_time": reservation_time.isoformat(),
            "duration_minutes": 60
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == "John Doe"
    assert data["table_id"] == table_fixture.id


def test_create_reservation_past_time(client: TestClient, table_fixture: Table):
    """Test creating a reservation with past time (should fail)."""
    past_time = datetime.now(table_fixture.created_at.tzinfo) - timedelta(days=1)
    response = client.post(
        "/api/v1/reservations/",
        json={
            "customer_name": "John Doe",
            "table_id": table_fixture.id,
            "reservation_time": past_time.isoformat(),
            "duration_minutes": 60
        }
    )
    assert response.status_code == 400
    assert "Reservation time must be in the future" in response.json()["detail"]


def test_create_reservation_invalid_table(client: TestClient):
    """Test creating a reservation for non-existent table."""
    response = client.post(
        "/api/v1/reservations/",
        json={
            "customer_name": "John Doe",
            "table_id": 999,
            "reservation_time": (
                datetime.now(UTC) + timedelta(hours=1)
            ).isoformat(),
            "duration_minutes": 60
        }
    )
    assert response.status_code == 400


def test_get_reservation(client: TestClient, reservation_fixture: dict):
    """Test getting a reservation by ID."""
    response = client.get(f"/api/v1/reservations/{reservation_fixture['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == reservation_fixture["id"]
    assert data["table_id"] == reservation_fixture["table_id"]


def test_update_reservation(client: TestClient, reservation_fixture: dict):
    """Test updating a reservation."""
    # Get the reservation to access its timezone info
    response = client.get(f"/api/v1/reservations/{reservation_fixture['id']}")
    reservation_data = response.json()
    
    # Parse the reservation_time from the response
    current_time = datetime.fromisoformat(reservation_data["reservation_time"])
    
    # Create new time using the same timezone
    new_time = datetime.now(current_time.tzinfo) + timedelta(days=2)
    
    response = client.put(
        f"/api/v1/reservations/{reservation_fixture['id']}",
        json={
            "customer_name": "Updated Customer",
            "reservation_time": new_time.isoformat(),
            "duration_minutes": 90
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["customer_name"] == "Updated Customer"
    assert data["duration_minutes"] == 90


def test_get_reservations(client: TestClient, db_session: Session):
    """Test getting all reservations."""
    # Create a test table first
    table_data = {
        "name": "Test Table",
        "seats": 4,
        "location": "Test Location"
    }
    table_response = client.post("/api/v1/tables/", json=table_data)
    assert table_response.status_code == 201
    table_id = table_response.json()["id"]

    # Create a test reservation
    reservation_time = datetime.now(UTC) + timedelta(hours=1)
    reservation_data = {
        "customer_name": "Test Customer",
        "reservation_time": reservation_time.isoformat(),
        "duration_minutes": 60,
        "table_id": table_id
    }
    reservation_response = client.post("/api/v1/reservations/", json=reservation_data)
    assert reservation_response.status_code == 201
    created_reservation = reservation_response.json()
    assert created_reservation["customer_name"] == "Test Customer"

    # Get all reservations
    response = client.get("/api/v1/reservations/")
    assert response.status_code == 200
    reservations = response.json()
    assert len(reservations) > 0
    assert reservations[0]["customer_name"] == "Test Customer"


def test_delete_reservation(client: TestClient, reservation_fixture: dict):
    """Test deleting a reservation."""
    response = client.delete(f"/api/v1/reservations/{reservation_fixture['id']}")
    assert response.status_code == 204


def test_reservation_time_conflict(client: TestClient, table_fixture: Table):
    """Test creating a reservation with time conflict."""
    # Create first reservation
    reservation_time = datetime.now(table_fixture.created_at.tzinfo) + timedelta(hours=1)
    first_response = client.post(
        "/api/v1/reservations/",
        json={
            "customer_name": "John Doe",
            "table_id": table_fixture.id,
            "reservation_time": reservation_time.isoformat(),
            "duration_minutes": 60
        }
    )
    assert first_response.status_code == 201

    # Try to create overlapping reservation
    response = client.post(
        "/api/v1/reservations/",
        json={
            "customer_name": "Jane Doe",
            "table_id": table_fixture.id,
            "reservation_time": (
                reservation_time + timedelta(minutes=30)
            ).isoformat(),
            "duration_minutes": 60
        }
    )
    assert response.status_code == 400 