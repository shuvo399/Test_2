import pytest
from fastapi.testclient import TestClient
import main

@pytest.fixture(autouse=True)
def clear_tickets():
    main.tickets.clear()
    yield
    main.tickets.clear()

@pytest.fixture
def client():
    return TestClient(main.app)

def sample_ticket(id=1):
    return {
        "id": id,
        "flight_name": "AirTest 100",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "Testville"
    }

def test_index(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"Message": "Welcome to the Ticket Booking System"}

def test_add_and_get_ticket(client):
    t = sample_ticket()
    resp = client.post("/ticket", json=t)
    assert resp.status_code == 200
    assert resp.json() == t

    resp = client.get("/ticket")
    assert resp.status_code == 200
    assert resp.json() == [t]

def test_update_ticket(client):
    t = sample_ticket(id=5)
    client.post("/ticket", json=t)

    updated = t.copy()
    updated["destination"] = "NewPlace"
    resp = client.put(f"/ticket/{t['id']}", json=updated)
    assert resp.status_code == 200
    assert resp.json() == updated

    resp = client.get("/ticket")
    assert resp.json() == [updated]

def test_update_nonexistent(client):
    updated = sample_ticket(id=999)
    resp = client.put("/ticket/999", json=updated)
    assert resp.status_code == 200
    assert resp.json() == {"error": "Ticket Not Found"}

def test_delete_ticket(client):
    t = sample_ticket(id=10)
    client.post("/ticket", json=t)

    resp = client.delete(f"/ticket/{t['id']}")
    assert resp.status_code == 200
    assert resp.json() == t

    resp = client.get("/ticket")
    assert resp.json() == []

def test_delete_nonexistent(client):
    resp = client.delete("/ticket/12345")
    assert resp.status_code == 200
    assert resp.json() == {"error": "Ticket not found, deletion failed"}
