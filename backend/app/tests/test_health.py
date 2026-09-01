"""Tests for the health endpoint."""
import pytest


def test_health_check(client):
    """Test that the health endpoint returns 200 with correct response."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "School Website" in data["app"]  # Should be "School Website" or "School Website Test"
    assert "database" in data


def test_root_endpoint(client):
    """Test the root endpoint returns application info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "status" in data
    assert data["status"] == "ready"
