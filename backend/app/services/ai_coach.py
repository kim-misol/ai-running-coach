from app.models import CoachFeedback, RacePrediction, RunningMetrics

# 실제 구현 시에는 LangChain이나 OpenAI SDK를 사용합니다.
# 여기서는 로직의 흐름을 보여드리기 위해 Mocking 합니다.


class AICoachService:
    """
    AI 러닝 코치 서비스.
    러닝 데이터를 분석하여 피드백과 예측을 제공합니다.
    """

    async def analyze_running_session(self, metrics: RunningMetrics) -> CoachFeedback:
        """
        러닝 세션을 분석하여 코칭 피드백을 생성합니다.

        Args:
            metrics (RunningMetrics): 러닝 데이터 객체

        Returns:
            CoachFeedback: 구조화된 피드백 데이터
        """

        # 1. Prompt Engineering (AI에게 보낼 프롬프트 구성)
        prompt = self._construct_prompt(metrics)

        # 2. Call LLM (여기서는 Mock 응답 반환)
        # response = await openai.ChatCompletion.create(...)

        # Mock Response
        return CoachFeedback(
            summary=f"{metrics.activity_date.date()}의 런닝은 훌륭했습니다. 심박수가 안정적입니다.",
            strength=["일정한 케이던스 유지", "초반 오버페이스 방지"],
            weakness=["후반부 심박수 급격한 상승"],
            suggested_workout="다음 세션은 존2(Zone 2) 영역에서의 60분 지속주를 추천합니다.",
            race_predictions=[
                RacePrediction(
                    distance_km=5, predicted_time_str="00:22:30", confidence_score=0.85
                ),
                RacePrediction(
                    distance_km=10, predicted_time_str="00:46:15", confidence_score=0.80
                ),
            ],
        )

    def _construct_prompt(self, metrics: RunningMetrics) -> str:
        return f"""
        당신은 전문 엘리트 러닝 코치입니다. 아래 데이터를 분석해주세요.
        
        - 거리: {metrics.distance_meters}m
        - 시간: {metrics.duration_seconds}초
        - 평균 심박: {metrics.average_heart_rate}
        - 페이스: {metrics.avg_pace}
        
        JSON 포맷으로 강점, 약점, 다음 훈련 추천, 5k/10k 예상 기록을 반환해주세요.
        """
