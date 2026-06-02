"""
Pytest configuration and fixtures for the API tests.
Provides a TestClient and isolated test data for each test.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient for making HTTP requests to the app.
    """
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """
    Fixture that resets activities to a clean state before each test.
    This ensures test isolation - changes in one test don't affect others.
    """
    # Store original state
    original_activities = {
        name: {
            "description": activity["description"],
            "schedule": activity["schedule"],
            "max_participants": activity["max_participants"],
            "participants": activity["participants"].copy()
        }
        for name, activity in activities.items()
    }
    
    yield activities
    
    # Restore original state after test
    for name in activities:
        activities[name]["participants"] = original_activities[name]["participants"].copy()
