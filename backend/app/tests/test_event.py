"""Tests for the event endpoints."""
from datetime import datetime, timedelta


class TestGetEvent:
    """Tests for GET /api/events."""

    def test_get_events_empty(self, client):
        """Test GET events when no events exist."""
        response = client.get("/api/events")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_event_not_found(self, client):
        """Test GET event when it does not exist."""
        response = client.get("/api/events/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Event not found"

    def test_get_event_found(self, client):
        """Test GET event when an event exists."""
        event_data = {
            "title": "Spring Fair",
            "description": "Annual school fair",
            "event_date": "2026-05-10T09:00:00",
            "location": "Main Hall",
            "published": True,
        }
        create_response = client.post("/api/events", json=event_data)
        assert create_response.status_code == 201

        response = client.get("/api/events/1")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Spring Fair"
        assert data["id"] == 1
        assert data["location"] == "Main Hall"
        assert "created_at" in data
        assert "updated_at" in data


class TestCreateEvent:
    """Tests for POST /api/events."""

    def test_create_event_success(self, client):
        """Test creating an event."""
        event_data = {
            "title": "Science Expo",
            "description": "School science project showcase",
            "event_date": "2026-06-15T10:30:00",
            "location": "Science Block",
            "published": False,
        }
        response = client.post("/api/events", json=event_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Science Expo"
        assert data["event_date"] == "2026-06-15T10:30:00"
        assert data["published"] is False

    def test_create_event_validation_error(self, client):
        """Test creating an event with invalid data."""
        response = client.post(
            "/api/events",
            json={
                "title": "",
                "description": "Bad event",
                "event_date": "2026-06-15T10:30:00",
                "location": "Hall",
            },
        )
        assert response.status_code == 422


class TestListEvents:
    """Tests for listing events."""

    def test_list_events_orders_by_event_date_desc(self, client):
        """Test events are returned sorted by most recent event date first."""
        earlier = "2026-02-10T09:00:00"
        later = "2026-07-12T09:00:00"
        client.post(
            "/api/events",
            json={
                "title": "Early Event",
                "description": "First event",
                "event_date": earlier,
                "location": "A",
            },
        )
        client.post(
            "/api/events",
            json={
                "title": "Later Event",
                "description": "Second event",
                "event_date": later,
                "location": "B",
            },
        )

        response = client.get("/api/events")
        assert response.status_code == 200
        items = response.json()
        assert [item["title"] for item in items] == ["Later Event", "Early Event"]


class TestUpdateEvent:
    """Tests for PUT /api/events/{event_id}."""

    def test_update_event_not_found(self, client):
        """Test updating an event that doesn't exist."""
        response = client.put(
            "/api/events/999",
            json={"title": "Updated event"},
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Event not found"

    def test_update_event_success(self, client):
        """Test updating an event with valid data."""
        client.post(
            "/api/events",
            json={
                "title": "Original Event",
                "description": "Original description",
                "event_date": "2026-04-01T09:00:00",
                "location": "Old Hall",
                "published": False,
            },
        )

        response = client.put(
            "/api/events/1",
            json={
                "title": "Updated Event",
                "description": "New description",
                "published": True,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Event"
        assert data["description"] == "New description"
        assert data["published"] is True

    def test_update_event_partial(self, client):
        """Test updating only some fields."""
        client.post(
            "/api/events",
            json={
                "title": "Original Event",
                "description": "Original description",
                "event_date": "2026-04-01T09:00:00",
                "location": "Old Hall",
            },
        )

        response = client.put(
            "/api/events/1",
            json={"location": "New Hall"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Original Event"
        assert data["location"] == "New Hall"


class TestDeleteEvent:
    """Tests for DELETE /api/events/{event_id}."""

    def test_delete_event_not_found(self, client):
        """Test deleting an event that doesn't exist."""
        response = client.delete("/api/events/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Event not found"

    def test_delete_event_success(self, client):
        """Test deleting an existing event."""
        client.post(
            "/api/events",
            json={
                "title": "Delete Me",
                "description": "Remove this",
                "event_date": "2026-04-01T09:00:00",
                "location": "Hall",
            },
        )

        response = client.delete("/api/events/1")
        assert response.status_code == 204

        get_response = client.get("/api/events/1")
        assert get_response.status_code == 404
