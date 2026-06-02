"""
Tests for the remove participant endpoints.
Uses the AAA (Arrange-Act-Assert) pattern for clarity.
"""

import pytest


class TestRemoveParticipant:
    """Test cases for POST /activities/{activity_name}/remove endpoint"""

    def test_remove_success(self, client, reset_activities):
        """
        Test that a participant can be successfully removed from an activity.

        AAA Pattern:
        - Arrange: Participant is currently signed up
        - Act: Send POST request to remove endpoint
        - Assert: Response is 200 and participant is removed
        """
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"
        initial_count = len(reset_activities[activity]["participants"])
        assert email in reset_activities[activity]["participants"]

        # Act
        response = client.post(
            f"/activities/{activity}/remove?email={email}",
            headers={"Content-Type": "application/json"}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Removed {email} from {activity}"
        assert email not in reset_activities[activity]["participants"]
        assert len(reset_activities[activity]["participants"]) == initial_count - 1

    def test_remove_nonexistent_participant(self, client, reset_activities):
        """
        Test that removing a non-existent participant fails.

        AAA Pattern:
        - Arrange: Email not signed up for activity
        - Act: Attempt to remove the participant
        - Assert: Response is 400 with not signed up error
        """
        # Arrange
        email = "notinlist@mergington.edu"
        activity = "Chess Club"
        # Ensure email is not in the activity
        assert email not in reset_activities[activity]["participants"]

        # Act
        response = client.post(
            f"/activities/{activity}/remove?email={email}",
            headers={"Content-Type": "application/json"}
        )

        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_remove_nonexistent_activity(self, client, reset_activities):
        """
        Test that removing from a non-existent activity fails.

        AAA Pattern:
        - Arrange: Non-existent activity name
        - Act: Attempt to remove from the activity
        - Assert: Response is 404 with activity not found error
        """
        # Arrange
        email = "student@mergington.edu"
        activity = "Nonexistent Activity"

        # Act
        response = client.post(
            f"/activities/{activity}/remove?email={email}",
            headers={"Content-Type": "application/json"}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_remove_updates_availability(self, client, reset_activities):
        """
        Test that available spots increase after removing a participant.

        AAA Pattern:
        - Arrange: Get initial participant count
        - Act: Remove a participant
        - Assert: Participant count decreases by 1
        """
        # Arrange
        email = "john@mergington.edu"
        activity = "Gym Class"
        initial_participants = len(reset_activities[activity]["participants"])

        # Act
        response = client.post(
            f"/activities/{activity}/remove?email={email}",
            headers={"Content-Type": "application/json"}
        )

        # Assert
        assert response.status_code == 200
        new_participants = len(reset_activities[activity]["participants"])
        assert new_participants == initial_participants - 1

    def test_remove_and_signup_again(self, client, reset_activities):
        """
        Test that a student can sign up again after being removed.

        AAA Pattern:
        - Arrange: Participant is signed up
        - Act: Remove and then sign up again
        - Assert: Participant is back in the activity
        """
        # Arrange
        email = "liam@mergington.edu"
        activity = "Basketball Team"
        assert email in reset_activities[activity]["participants"]

        # Act - Remove
        response_remove = client.post(
            f"/activities/{activity}/remove?email={email}",
            headers={"Content-Type": "application/json"}
        )
        assert response_remove.status_code == 200
        assert email not in reset_activities[activity]["participants"]

        # Act - Sign up again
        response_signup = client.post(
            f"/activities/{activity}/signup?email={email}",
            headers={"Content-Type": "application/json"}
        )

        # Assert
        assert response_signup.status_code == 200
        assert email in reset_activities[activity]["participants"]
