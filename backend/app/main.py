from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException

from app.models import AnalysisRequest, CoachFeedback
from app.services.ai_coach import AICoachService
from app.services.garmin_service import GarminService  # 가상의 서비스

app = FastAPI(
    title="AI Running Coach API",
    description="Garmin 데이터를 분석하여 러닝 피드백을 제공하는 API",
    version="1.0.0",
)


# Dependency Injection
def get_ai_coach() -> AICoachService:
    return AICoachService()


def get_garmin_service() -> GarminService:
    return GarminService()


@app.get("/")
async def health_check():
    """서버 상태 확인용 헬스 체크"""
    return {"status": "ok", "timestamp": datetime.now()}


@app.post(
    "/api/v1/analyze",
    response_model=CoachFeedback,
    summary="러닝 데이터 분석 요청",
    description="Garmin 활동 ID를 받아 데이터를 가져온 후 AI 코칭 결과를 반환합니다.",
)
async def analyze_workout(
    request: AnalysisRequest,
    coach: AICoachService = Depends(get_ai_coach),
    garmin: GarminService = Depends(get_garmin_service),
):
    # 1. Garmin 데이터 Fetch
    activity_data = await garmin.get_activity(request.activity_id)

    if not activity_data:
        raise HTTPException(status_code=404, detail="Activity not found")

    # 2. AI 분석 수행
    feedback = await coach.analyze_running_session(activity_data)

    return feedback


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
