from datetime import datetime

from app.models import RunningMetrics


class GarminService:
    async def get_activity(
        self, activity_id: str
    ) -> RunningMetrics:  # Mock Data for now return
        RunningMetrics(
            distance_meters=10020,
            duration_seconds=2950,
            average_heart_rate=155,
            max_heart_rate=178,
            calories=750,
            avg_pace=4.91,
            activity_date=datetime.now(),
        )
