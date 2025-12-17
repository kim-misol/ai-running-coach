# backend/tests/conftest.py
from datetime import datetime

import pytest

from app.models import RunningMetrics


# Mock data fixture for RunningMetrics
@pytest.fixture
def mock_running_metrics():
    return RunningMetrics(
        distance_meters=5000.0,
        duration_seconds=1500.0,
        average_heart_rate=150,
        max_heart_rate=180,
        calories=400,
        avg_pace=5.0,
        activity_date=datetime(2024, 1, 1, 10, 0, 0),
    )


# Mock Garmin activity data (Raw JSON)
@pytest.fixture
def mock_garmin_json():
    return {
        "activityName": "Morning Run",
        "distance": 5000.0,
        "duration": 1500.0,
        "averageHR": 150,
        "maxHR": 180,
        "calories": 400,
        "averageSpeed": 3.33,  # m/s (approx 5:00 min/km)
        "startTimeLocal": "2024-01-01 10:00:00",
    }
