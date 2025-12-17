from fastapi.testclient import TestClient

from app.main import app, get_garmin_service
from app.models import RunningMetrics

client = TestClient(app)


# 가민 서비스를 흉내내는 Mock Class
class MockGarminService:
    async def get_activity(self, activity_id: str):
        from datetime import datetime

        return RunningMetrics(
            distance_meters=10000.0,
            duration_seconds=3000.0,
            average_heart_rate=160,
            max_heart_rate=185,
            calories=800,
            avg_pace=5.0,
            activity_date=datetime.now(),
        )


# 의존성 오버라이드 적용
app.dependency_overrides[get_garmin_service] = MockGarminService


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_endpoint():
    payload = {"user_id": "test_user", "activity_id": "12345"}
    response = client.post("/api/v1/analyze", json=payload)

    assert response.status_code == 200
    data = response.json()

    # 필수 필드 존재 여부 확인
    assert "summary" in data
    assert "metrics" in data
    assert "chart_data" in data
    assert data["metrics"]["distance_meters"] == 10000.0
