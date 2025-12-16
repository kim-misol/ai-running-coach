from datetime import datetime
from typing import Any, Dict, List

from fastapi import Depends, FastAPI, HTTPException

from app.models import AnalysisRequest, CoachFeedback, RunningMetrics
from app.services.ai_coach import AICoachService
from app.services.garmin_service import GarminService

app = FastAPI(
    title="AI Running Coach API",
    description="Garmin 데이터를 분석하여 러닝 피드백을 제공하는 API",
    version="1.0.0",
)


# 프론트엔드 AnalysisResponse와 일치하는 응답 모델 정의
class FullAnalysisResponse(CoachFeedback):
    metrics: RunningMetrics
    chart_data: List[Dict[str, Any]]


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
    response_model=FullAnalysisResponse,
    summary="러닝 데이터 분석 요청",
    description="Garmin 활동 ID를 받아 데이터를 가져온 후 AI 코칭 결과를 반환합니다.",
)
async def analyze_workout(
    request: AnalysisRequest,
    coach: AICoachService = Depends(get_ai_coach),
    garmin: GarminService = Depends(get_garmin_service),
):
    # 1. Garmin 데이터 Fetch
    try:
        activity_data = await garmin.get_activity(request.activity_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Garmin Error: {str(e)}")

    if not activity_data:
        raise HTTPException(status_code=404, detail="Activity not found")

    # 2. AI 분석 수행
    feedback = await coach.analyze_running_session(activity_data)

    # 3. 차트 데이터 생성 (현재는 AI 서비스 내부 메서드로 시뮬레이션)
    chart_data = coach._generate_chart_data_from_real_metrics(activity_data)

    # 4. 프론트엔드 포맷에 맞춰 데이터 합치기
    # Pydantic 모델 -> Dict 변환 후 병합
    response_data = feedback.model_dump()
    response_data["metrics"] = activity_data
    response_data["chart_data"] = chart_data

    return response_data


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
