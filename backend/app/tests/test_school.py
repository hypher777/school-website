"""Tests for the school endpoints."""
import pytest


class TestGetSchool:
    """Tests for GET /api/school."""

    def test_get_school_not_found(self, admin_client):
        """Test GET school when no school exists."""
        response = admin_client.get("/api/school")
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "School not found"

    def test_get_school_found(self, admin_client):
        """Test GET school when a school exists."""
        # First create a school
        school_data = {
            "name": "Test School",
            "description": "A test school",
            "address": "123 Main St",
            "phone": "555-1234",
            "email": "test@school.com",
            "logo_url": "https://example.com/logo.png",
            "established_year": 2000,
        }
        admin_client.post("/api/school", json=school_data)

        # Then get it
        response = admin_client.get("/api/school")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test School"
        assert data["id"] == 1
        assert "created_at" in data
        assert "updated_at" in data


class TestCreateSchool:
    """Tests for POST /api/school."""

    def test_create_school_success(self, admin_client):
        """Test creating a school."""
        school_data = {
            "name": "New School",
            "description": "A new school",
            "address": "456 Oak Ave",
            "phone": "555-5678",
            "email": "new@school.com",
            "logo_url": "https://example.com/logo2.png",
            "established_year": 2010,
        }
        response = admin_client.post("/api/school", json=school_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "New School"
        assert data["id"] == 1

    def test_create_school_minimal(self, admin_client):
        """Test creating a school with only required field."""
        school_data = {"name": "Minimal School"}
        response = admin_client.post("/api/school", json=school_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Minimal School"
        assert data["description"] is None

    def test_create_school_duplicate_conflict(self, admin_client):
        """Test that creating a second school returns 409 Conflict."""
        school_data = {"name": "First School"}
        response1 = admin_client.post("/api/school", json=school_data)
        assert response1.status_code == 201

        # Try to create a second school
        school_data2 = {"name": "Second School"}
        response2 = admin_client.post("/api/school", json=school_data2)
        assert response2.status_code == 409
        data = response2.json()
        assert "already exists" in data["detail"]

    def test_create_school_validation_error(self, admin_client):
        """Test creating a school with invalid data."""
        school_data = {"name": ""}  # Empty name should fail
        response = admin_client.post("/api/school", json=school_data)
        assert response.status_code == 422  # Validation error


class TestUpdateSchool:
    """Tests for PUT /api/school."""

    def test_update_school_not_found(self, admin_client):
        """Test updating a school that doesn't exist."""
        response = admin_client.put(
            "/api/school", json={"name": "Updated School"}
        )
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "School not found"

    def test_update_school_success(self, admin_client):
        """Test updating a school with new data."""
        # Create a school
        create_data = {"name": "Original School", "description": "Original"}
        admin_client.post("/api/school", json=create_data)

        # Update it
        update_data = {
            "name": "Updated School",
            "description": "Updated description",
        }
        response = admin_client.put("/api/school", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated School"
        assert data["description"] == "Updated description"

    def test_update_school_partial(self, admin_client):
        """Test updating only some fields."""
        # Create a school
        create_data = {
            "name": "Original",
            "description": "Original desc",
            "phone": "555-1111",
        }
        admin_client.post("/api/school", json=create_data)

        # Update only phone
        response = admin_client.put("/api/school", json={"phone": "555-2222"})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Original"  # Unchanged
        assert data["description"] == "Original desc"  # Unchanged
        assert data["phone"] == "555-2222"  # Updated

    def test_update_school_empty_request(self, admin_client):
        """Test updating with no fields returns school as-is."""
        # Create a school
        create_data = {"name": "Test School"}
        admin_client.post("/api/school", json=create_data)

        # Update with no data
        response = admin_client.put("/api/school", json={})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test School"


class TestDeleteSchool:
    """Tests for DELETE /api/school."""

    def test_delete_school_not_found(self, admin_client):
        """Test deleting a school that doesn't exist."""
        response = admin_client.delete("/api/school")
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "School not found"

    def test_delete_school_success(self, admin_client):
        """Test deleting an existing school."""
        # Create a school
        create_data = {"name": "School to Delete"}
        admin_client.post("/api/school", json=create_data)

        # Delete it
        response = admin_client.delete("/api/school")
        assert response.status_code == 204

        # Verify it's gone
        response = admin_client.get("/api/school")
        assert response.status_code == 404

    def test_delete_then_create_new(self, admin_client):
        """Test that after deletion, a new school can be created."""
        # Create a school
        admin_client.post("/api/school", json={"name": "First"})

        # Delete it
        admin_client.delete("/api/school")

        # Create a new one (should work since old one is deleted)
        response = admin_client.post("/api/school", json={"name": "Second"})
        assert response.status_code == 201
        assert response.json()["name"] == "Second"
