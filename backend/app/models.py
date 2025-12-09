from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class ActivityType(str, Enum):
    RUNNING = "running"
    CYCLING = "cycling"
    SWIMMING = "swimming"


class RunningMetrics(BaseModel):
    """러닝 활동의 핵심 지표 데이터 모델"""

    distance_meters: float = Field(..., description="이동 거리 (미터)")
    duration_seconds: float = Field(..., description="운동 시간 (초)")
    average_heart_rate: Optional[int] = Field(None, description="평균 심박수")
    max_heart_rate: Optional[int] = Field(None, description="최대 심박수")
    calories: int = Field(..., description="소모 칼로리")
    avg_pace: float = Field(..., description="평균 페이스 (분/km)")
    activity_date: datetime = Field(..., description="활동 날짜")


class RacePrediction(BaseModel):
    """AI가 예측한 레이스 기록"""

    distance_km: float
    predicted_time_str: str = Field(..., description="예상 기록 (예: '00:45:30')")
    confidence_score: float = Field(..., ge=0, le=1, description="예측 신뢰도")


class CoachFeedback(BaseModel):
    """AI 코치의 최종 피드백 응답 모델"""

    summary: str = Field(..., description="훈련 요약")
    strength: List[str] = Field(..., description="잘한 점")
    weakness: List[str] = Field(..., description="보완할 점")
    suggested_workout: str = Field(..., description="다음 추천 훈련")
    race_predictions: List[RacePrediction] = Field(..., description="거리별 예상 기록")


class AnalysisRequest(BaseModel):
    user_id: str
    activity_id: str
