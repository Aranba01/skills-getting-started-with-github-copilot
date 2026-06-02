"""
Tests for the activities endpoints.
Uses the AAA (Arrange-Act-Assert) pattern for clarity.
"""

import pytest


class TestGetActivities:
    """Test cases for GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """
        Test that GET /activities returns all available activities.

        AAA Pattern:
        - Arrange: Client is ready (fixture)
        - Act: Make GET request to /activities
        - Assert: Response has status 200 and contains all activities
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Yoga Club",
            "Art Studio",
            "Drama Club",
            "Math Olympiad",
            "Science Club"
        ]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        for activity_name in expected_activities:
            assert activity_name in activities

    def test_get_activities_structure(self, client, reset_activities):
        """
        Test that each activity has the correct structure.

        AAA Pattern:
        - Arrange: Expected fields for an activity
        - Act: Get activities and inspect first one
        - Assert: First activity has all required fields
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")
        activities = response.json()
        first_activity = activities["Chess Club"]

        # Assert
        for field in required_fields:
            assert field in first_activity
        assert isinstance(first_activity["participants"], list)
        assert isinstance(first_activity["max_participants"], int)

    def test_get_activities_participants_are_emails(self, client, reset_activities):
        """
        Test that participants are stored as email strings.

        AAA Pattern:
        - Arrange: Get activities
        - Act: Fetch and inspect a participant
        - Assert: Participant is a valid email string
        """
        # Arrange & Act
        response = client.get("/activities")
        activities = response.json()
        participants = activities["Chess Club"]["participants"]

        # Assert
        assert len(participants) > 0
        for participant in participants:
            assert isinstance(participant, str)
            assert "@" in participant
            assert ".edu" in participant


class TestRootRedirect:
    """Test cases for GET / endpoint"""

    def test_root_redirects_to_static_index(self, client):
        """
        Test that GET / redirects to /static/index.html.

        AAA Pattern:
        - Arrange: Client is ready
        - Act: Make GET request to root with follow_redirects=False
        - Assert: Response is a 307 redirect to /static/index.html
        """
        # Arrange & Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"
