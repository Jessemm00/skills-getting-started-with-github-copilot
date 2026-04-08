"""
Tests for signup and unregister endpoints.
Uses the AAA (Arrange-Act-Assert) pattern to structure tests.
"""
import pytest


class TestSignupForActivity:
    """Test suite for signing up for activities."""

    def test_signup_successful_adds_participant(self, client, reset_activities):
        """Test that a student can successfully sign up for an activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        initial_count = len(client.get("/activities").json()[activity_name]["participants"])

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        
        # Verify participant was added
        activities = client.get("/activities").json()
        assert email in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_count + 1

    def test_signup_returns_confirmation_message(self, client, reset_activities):
        """Test that signup response contains a confirmation message."""
        # Arrange
        activity_name = "Programming Class"
        email = "alice@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_nonexistent_activity_returns_404(self, client):
        """Test that signing up for a non-existent activity returns 404."""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_duplicate_registration_prevented(self, client, reset_activities):
        """Test that a student cannot register twice for the same activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "student@mergington.edu"
        
        # First signup
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Act - Try to sign up again
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "already" in response.json()["detail"].lower()

    def test_signup_multiple_different_students(self, client, reset_activities):
        """Test that multiple different students can sign up for the same activity."""
        # Arrange
        activity_name = "Gym Class"
        student1 = "student1@mergington.edu"
        student2 = "student2@mergington.edu"

        # Act
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student1}
        )
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student2}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        activities = client.get("/activities").json()
        assert student1 in activities[activity_name]["participants"]
        assert student2 in activities[activity_name]["participants"]


class TestUnregisterFromActivity:
    """Test suite for unregistering from activities."""

    def test_unregister_successful_removes_participant(self, client, reset_activities):
        """Test that a student can successfully unregister from an activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Sign up first
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        initial_count = len(client.get("/activities").json()[activity_name]["participants"])

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert email not in response.json()["message"]
        
        # Verify participant was removed
        activities = client.get("/activities").json()
        assert email not in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_count - 1

    def test_unregister_nonexistent_student_returns_400(self, client):
        """Test that unregistering a student who isn't signed up returns 400."""
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"].lower()

    def test_unregister_nonexistent_activity_returns_404(self, client):
        """Test that unregistering from a non-existent activity returns 404."""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_returns_confirmation_message(self, client, reset_activities):
        """Test that unregister response contains a confirmation message."""
        # Arrange
        activity_name = "Programming Class"
        email = "student@mergington.edu"
        
        # Sign up first
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]
