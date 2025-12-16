import logging
from datetime import datetime

from garminconnect import Garmin

from app.core.config import settings
from app.models import RunningMetrics

# 로깅 설정
logger = logging.getLogger("uvicorn")

## Dummy GarminService for testing without real Garmin API
# class GarminService:
#     async def get_activity(
#         self, activity_id: str
#     ) -> RunningMetrics:  # Mock Data for now return
#         RunningMetrics(
#             distance_meters=10020,
#             duration_seconds=2950,
#             average_heart_rate=155,
#             max_heart_rate=178,
#             calories=750,
#             avg_pace=4.91,
#             activity_date=datetime.now(),
#         )


class GarminService:
    def __init__(self):
        self.email = settings.GARMIN_EMAIL
        self.password = settings.GARMIN_PASSWORD
        self.client = None

    def _login(self):
        """가민 클라이언트에 로그인합니다."""
        try:
            self.client = Garmin(self.email, self.password)
            self.client.login()
            logger.info("✅ Garmin Login Successful")
        except Exception as e:
            logger.error(f"❌ Garmin Login Failed: {str(e)}")
            raise e

    def _calculate_pace(self, speed_mps: float) -> float:
        """m/s 단위를 분/km 단위로 변환합니다."""
        if not speed_mps or speed_mps <= 0:
            return 0.0
        # 1 m/s = 16.666... min/km (1000m / 60sec) 역산
        # Pace (min/km) = 16.6666 / speed (m/s)
        minutes_per_km = 16.666666666667 / speed_mps
        return round(minutes_per_km, 2)

    async def get_activity(self, activity_id: str) -> RunningMetrics:
        """
        가민에서 가장 최근 활동 1개를 가져옵니다.
        (activity_id 인자는 현재 데모용으로 무시하고 가장 최신 것을 가져옵니다)
        """
        if not self.client:
            self._login()

        try:
            # 최근 활동 1개 가져오기 (0번 인덱스부터 1개)
            activities = self.client.get_activities(0, 1)

            if not activities:
                raise Exception("No activities found")

            # 가장 최근 활동 데이터 (Raw JSON)
            latest_activity = activities[0]

            logger.info(
                f"🏃 Fetching activity: {latest_activity.get('activityName', 'Unknown')}"
            )

            # 가민 데이터 -> 우리 앱 모델로 매핑
            metrics = RunningMetrics(
                distance_meters=latest_activity.get("distance", 0),
                duration_seconds=latest_activity.get("duration", 0),
                average_heart_rate=latest_activity.get("averageHR", 0),
                max_heart_rate=latest_activity.get("maxHR", 0),
                calories=latest_activity.get("calories", 0),
                # 가민은 averageSpeed(m/s)를 줍니다. 이를 페이스(분/km)로 변환 필요
                avg_pace=self._calculate_pace(latest_activity.get("averageSpeed", 0)),
                # startTimeLocal 형식: "2024-05-20 07:00:00"
                activity_date=datetime.strptime(
                    latest_activity.get("startTimeLocal"), "%Y-%m-%d %H:%M:%S"
                ),
            )

            return metrics

        except Exception as e:
            logger.error(f"❌ Failed to fetch activity: {str(e)}")
            raise e
