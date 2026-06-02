"""
Tests for the signup endpoints.
Uses the AAA (Arrange-Act-Assert) pattern for clarity.
"""

import pytest


class TestSignup:
    """Test cases for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self, client, reset_activities):
        """
        Test that a student can successfully sign up for an activity.

        AAA Pattern:
        - Arrange: Prepare email and activity name
        - Act: Send POST request to signup endpoint
        - Assert: Response is 200 and participant is added
        """
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Chess Club"
        initial_count = len(reset_activities[activity]["participants"])

        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}",
            headers={"Content-Type": "application/json"}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity}"
        assert email in reset_activities[activity]["participants"]
        assert len(reset_activities[activity]["participants"]) == initial_count + 1

    def test_signup_duplicate_error(self, client, reset_activities):
        """
        Test that signing up twice for the same activity fails.

        AAA Pattern:
        - Arrange: Student email already signed up
        - Act: Attempt to sign up the same student again
        - Assert: Response is 400 with duplicate error
        """
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"
        # michael@mergington.edu is already in Chess Club

        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}",
            headers={"Content-Type": "application/json"}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_nonexistent_activity(self, client, reset_activities):
        """
        Test that signing up for a non-existent activity fails.

        AAA Pattern:
        - Arrange: Non-existent activity name
        - Act: Attempt to sign up for the activity
        - Assert: Response is 404 with activity not found error
        """
        # Arrange
        email = "student@mergington.edu"
        activity = "Nonexistent Activity"

        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}",
            headers={"Content-Type": "application/json"}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_updates_availability(self, client, reset_activities):
        """
        Test that available spots decrease after signup.

        AAA Pattern:
        - Arrange: Get initial participant count
        - Act: Sign up a new student
        - Assert: Participant count increases by 1
        """
        # Arrange
        email = "newsignup@mergington.edu"
        activity = "Yoga Club"
        initial_participants = len(reset_activities[activity]["participants"])
        max_participants = reset_activities[activity]["max_participants"]

        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}",
            headers={"Content-Type": "application/json"}
        )

        # Assert
        assert response.status_code == 200
        new_participants = len(reset_activities[activity]["participants"])
        assert new_participants == initial_participants + 1
        assert new_participants <= max_participants

    def test_signup_multiple_activities(self, client, reset_activities):
        """
        Test that a student can sign up for multiple different activities.

        AAA Pattern:
        - Arrange: Same email, different activities
        - Act: Sign up for multiple activities
        - Assert: Student is added to all activities
        """
        # Arrange
        email = "versatile@mergington.edu"
        activities_to_join = ["Chess Club", "Programming Class", "Yoga Club"]

        # Act
        for activity in activities_to_join:
            response = client.post(
                f"/activities/{activity}/signup?email={email}",
                headers={"Content-Type": "application/json"}
            )
            assert response.status_code == 200

        # Assert
        for activity in activities_to_join:
            assert email in reset_activities[activity]["participants"]
