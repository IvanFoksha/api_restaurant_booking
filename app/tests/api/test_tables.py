from fastapi.testclient import TestClient

from app.models.table import Table


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


def test_get_tables(client: TestClient, table_fixture: Table):
    """Test getting all tables."""
    response = client.get("/api/v1/tables/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == table_fixture.name


def test_delete_table(client: TestClient, table_fixture: Table):
    """Test deleting a table."""
    response = client.delete(f"/api/v1/tables/{table_fixture.id}")
    assert response.status_code == 204

    # Verify the table is deleted
    response = client.get(f"/api/v1/tables/{table_fixture.id}")
    assert response.status_code == 404


def test_create_table_without_location(client: TestClient):
    """Test creating a table without location (should use default)."""
    response = client.post(
        "/api/v1/tables/",
        json={
            "name": "Table 1",
            "seats": 4
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Table 1"
    assert data["seats"] == 4
    assert data["location"] == "Main Hall"


def test_get_table(client: TestClient, table_fixture: Table):
    """Test getting a table by ID."""
    response = client.get(f"/api/v1/tables/{table_fixture.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == table_fixture.name
    assert data["seats"] == table_fixture.seats
    assert data["location"] == table_fixture.location


def test_update_table(client: TestClient, table_fixture: Table):
    """Test updating a table."""
    response = client.put(
        f"/api/v1/tables/{table_fixture.id}",
        json={
            "name": "Updated Table",
            "seats": 6,
            "location": "Garden"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Table"
    assert data["seats"] == 6
    assert data["location"] == "Garden" 