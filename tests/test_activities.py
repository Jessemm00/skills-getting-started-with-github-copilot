"""
Tests for the GET /activities endpoint.
Uses the AAA (Arrange-Act-Assert) pattern to structure tests.
"""
import pytest


class TestGetActivities:
    """Test suite for retrieving all activities."""

    def test_get_all_activities_returns_success(self, client):
        """Test that the activities endpoint returns a 200 status code."""
        # Arrange
        # (no setup needed - activities are already in the app)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200

    def test_get_all_activities_returns_dict(self, client):
        """Test that the activities endpoint returns a dictionary."""
        # Arrange
        # (no setup needed)

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert isinstance(data, dict)

    def test_get_all_activities_contains_expected_fields(self, client):
        """Test that each activity has the required fields."""
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert required_fields.issubset(activity_data.keys())
            assert isinstance(activity_data["participants"], list)

    def test_get_all_activities_has_multiple_activities(self, client):
        """Test that the endpoint returns multiple activities."""
        # Arrange
        expected_minimum_activities = 3

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert len(activities) >= expected_minimum_activities

    def test_get_all_activities_participants_are_strings(self, client):
        """Test that all participants are stored as strings (emails)."""
        # Arrange
        # (no setup needed)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
                assert "@" in participant  # Verify email format
