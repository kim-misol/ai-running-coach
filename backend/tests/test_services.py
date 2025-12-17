import pytest

from app.services.ai_coach import AICoachService
from app.services.garmin_service import GarminService


@pytest.mark.asyncio
async def test_garmin_service_pace_calculation():
    service = GarminService()
    # 3.33 m/s는 약 5.0 min/km 여야 함
    pace = service._calculate_pace(3.333333)
    assert 4.9 < pace < 5.1


@pytest.mark.asyncio
async def test_ai_coach_chart_generation(mock_running_metrics):
    service = AICoachService()
    chart_data = service._generate_chart_data_from_real_metrics(mock_running_metrics)

    assert len(chart_data) > 0
    assert "heart_rate" in chart_data[0]
    assert "pace" in chart_data[0]
    # 생성된 심박수가 범위 내에 있는지 확인
    assert 100 <= chart_data[0]["heart_rate"] <= 200
