import random
from typing import Dict, List

from app.models import CoachFeedback, RacePrediction, RunningMetrics


class AICoachService:
    """
    AI 러닝 코치 서비스.
    러닝 데이터를 분석하여 피드백과 예측을 제공합니다.
    """

    def _generate_chart_data_from_real_metrics(
        self, metrics: RunningMetrics
    ) -> List[Dict]:
        """
        실제 요약 데이터를 기반으로 그럴듯한 차트 데이터를 생성합니다.
        (추후 가민 Activity Details API로 교체 예정)
        """
        data = []
        duration_min = int(metrics.duration_seconds / 60)
        points = min(duration_min, 100)  # 최대 100개 포인트
        interval = metrics.duration_seconds / points

        current_hr = metrics.average_heart_rate - 10
        current_pace = metrics.avg_pace

        for i in range(points):
            # 랜덤 변동성 추가
            current_hr += random.uniform(-2, 3)
            # 최대/최소 심박수 범위 제한
            current_hr = max(min(current_hr, metrics.max_heart_rate or 190), 100)

            # 페이스 변동
            current_pace += random.uniform(-0.2, 0.2)

            data.append(
                {
                    "time_offset": int(i * interval),
                    "heart_rate": int(current_hr),
                    "pace": round(current_pace, 2),
                }
            )

        return data

    async def analyze_running_session(self, metrics: RunningMetrics) -> CoachFeedback:
        """
        AI 분석 로직
        러닝 세션을 분석하여 코칭 피드백을 생성합니다.
        실제로는 OpenAI API를 호출해야 하지만, 여기서는 로직 템플릿만 유지합니다.

        Args:
            metrics (RunningMetrics): 러닝 데이터 객체

        Returns:
            CoachFeedback: 구조화된 피드백 데이터
        """

        # 실제 데이터 기반 차트 생성
        chart_data = self._generate_chart_data_from_real_metrics(metrics)

        # 동적 피드백 생성
        date_str = metrics.activity_date.strftime("%Y-%m-%d")
        dist_km = round(metrics.distance_meters / 1000, 2)

        # 1. Prompt Engineering (AI에게 보낼 프롬프트 구성)
        prompt = self._construct_prompt(metrics)

        # 2. Call LLM (여기서는 Mock 응답 반환)
        # response = await openai.ChatCompletion.create(...)

        # Mock Response
        return CoachFeedback(
            summary=f"[{date_str}] {dist_km}km 러닝 분석 완료. \
                평균 심박수 {metrics.average_heart_rate}bpm으로 수행했습니다.",
            strength=["목표 거리 완주", "안정적인 평균 페이스"],
            weakness=["데이터 기반 상세 분석 필요"],
            suggested_workout="회복 러닝 5km",
            race_predictions=[
                RacePrediction(
                    distance_km=5, predicted_time_str="00:25:00", confidence_score=0.8
                ),
                RacePrediction(
                    distance_km=10, predicted_time_str="00:52:00", confidence_score=0.75
                ),
            ],
            # Pydantic 모델에 정의되지 않은 필드는 무시되거나 별도 처리가 필요할 수 있으나,
            # FastAPI가 ResponseModel 변환 시 자동으로 합쳐주도록 Controller에서 처리하거나
            # CoachFeedback 모델에 chart_data 필드를 추가해야 할 수도 있습니다.
            # *중요*: 프론트엔드는 'metrics'와 'chart_data'를 따로 받지 않고
            # AnalysisResponse 타입 하나로 받고 있으므로, 백엔드 리턴값을 맞춰줘야 합니다.
        )

    # 실제 구현 시에는 LangChain이나 OpenAI SDK를 사용합니다.
    # 여기서는 로직의 흐름을 보여드리기 위해 Mocking 합니다.

    def _construct_prompt(self, metrics: RunningMetrics) -> str:
        return f"""
        당신은 전문 엘리트 러닝 코치입니다. 아래 데이터를 분석해주세요.
        
        - 거리: {metrics.distance_meters}m
        - 시간: {metrics.duration_seconds}초
        - 평균 심박: {metrics.average_heart_rate}
        - 페이스: {metrics.avg_pace}
        
        JSON 포맷으로 강점, 약점, 다음 훈련 추천, 5k/10k 예상 기록을 반환해주세요.
        """
