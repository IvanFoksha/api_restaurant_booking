from datetime import datetime, timedelta

from fastapi.testclient import TestClient


def test_create_table(client: TestClient):
    response = client.post(
        "/tables/",
        json={
            "number": 1,
            "capacity": 4,
            "location": "Window",
            "is_available": True
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["number"] == 1
    assert data["capacity"] == 4
    assert data["location"] == "Window"
    assert data["is_available"] is True


def test_get_tables(client: TestClient, table):
    response = client.get("/tables/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["number"] == table.number
    assert data[0]["capacity"] == table.capacity


def test_create_reservation(client: TestClient, table):
    response = client.post(
        "/reservations/",
        json={
            "table_id": table.id,
            "guest_name": "Test Guest",
            "guest_email": "test@example.com",
            "guest_phone": "+1234567890",
            "party_size": 2,
            "reservation_time": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "duration": 120,
            "status": "pending"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["table_id"] == table.id
    assert data["guest_name"] == "Test Guest"
    assert data["guest_email"] == "test@example.com"


def test_get_reservations(client: TestClient, reservation):
    response = client.get("/reservations/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == reservation.id
    assert data[0]["table_id"] == reservation.table_id


def test_reservation_conflict(client: TestClient, table):
    # Create first reservation
    first_reservation_time = datetime.utcnow() + timedelta(days=1)
    client.post(
        "/reservations/",
        json={
            "table_id": table.id,
            "guest_name": "First Guest",
            "guest_email": "first@example.com",
            "guest_phone": "+1234567890",
            "party_size": 2,
            "reservation_time": first_reservation_time.isoformat(),
            "duration": 120,
            "status": "pending"
        }
    )

    # Try to create conflicting reservation
    response = client.post(
        "/reservations/",
        json={
            "table_id": table.id,
            "guest_name": "Second Guest",
            "guest_email": "second@example.com",
            "guest_phone": "+0987654321",
            "party_size": 2,
            "reservation_time": (first_reservation_time + timedelta(minutes=60)).isoformat(),
            "duration": 120,
            "status": "pending"
        }
    )
    assert response.status_code == 400
    assert "conflict" in response.json()["detail"].lower()
