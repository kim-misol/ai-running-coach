// hooks/useRunningData.ts
import { useQuery } from "@tanstack/react-query";
import { AnalysisResponse, TimeSeriesDataPoint } from "@/lib/types";

// 더미 차트 데이터 생성 함수
const generateMockChartData = (): TimeSeriesDataPoint[] => {
  const data: TimeSeriesDataPoint[] = [];
  let currentHr = 130;
  let currentPace = 5.5; // 5분 30초

  for (let i = 0; i < 60; i++) { // 60개의 데이터 포인트 (약 1분 간격이라 가정)
    // 약간의 랜덤성을 부여하여 리얼하게 만듦
    currentHr += Math.random() * 4 - 1.5; 
    currentPace += Math.random() * 0.2 - 0.1;
    
    // 후반부 심박수 급상승 시뮬레이션 (AI 분석 내용과 일치시킴)
    if (i > 45) currentHr += 2; 

    data.push({
      time_offset: i * 60,
      heart_rate: Math.round(currentHr),
      pace: parseFloat(currentPace.toFixed(2)),
    });
  }
  return data;
};

// 실제 API 호출
const fetchAnalysis = async (): Promise<AnalysisResponse> => {
  // 개발 단계에서는 Mock Data를 리턴하거나 실제 API 호출
  // const res = await fetch('/api/v1/analyze/...'); 
  // 1. POST 요청 보내기
  // (Proxy 설정 덕분에 http://localhost:8000 을 생략하고 /api/... 만 쓰면 됩니다)
  const res = await fetch("/api/v1/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    // 현재 백엔드 로직상 activity_id는 무시하고 "가장 최신 활동"을 가져오므로
    // 임의의 값을 보내도 상관없습니다.
    body: JSON.stringify({
      user_id: "current_user",
      activity_id: "latest_activity", 
    }),
  });

  // 2. Error Handling
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Failed to fetch running analysis");
  }

  return res.json();
  // // Mock Data for UX Development
  // return new Promise((resolve) => {
  //   setTimeout(() => {
  //     resolve({
  //       summary: "오늘 훈련은 아주 훌륭했습니다. 심박수가 안정적이며 케이던스가 일정합니다.",
  //       strength: ["일정한 케이던스 (178spm)", "초반 오버페이스 방지 성공"],
  //       weakness: ["5km 이후 심박수 급격한 상승", "오르막 구간 페이스 저하"],
  //       suggested_workout: "내일은 회복을 위해 Zone 2 영역에서 40분 조깅을 권장합니다.",
  //       race_predictions: [
  //         { distance_km: 5, predicted_time_str: "00:22:30", confidence_score: 0.85 },
  //         { distance_km: 10, predicted_time_str: "00:46:15", confidence_score: 0.80 },
  //       ],
  //       metrics: {
  //         distance_meters: 10020,
  //         duration_seconds: 2950, // 약 49분
  //         average_heart_rate: 155,
  //         max_heart_rate: 178,
  //         calories: 750,
  //         avg_pace: 4.91, // 약 4분 55초
  //         activity_date: "2024-05-20T07:00:00"
  //       }, // 여기에 차트 데이터 추가
  //       chart_data: generateMockChartData()
  //     });
  //   }, 1000); // 1초 딜레이 시뮬레이션
  // });
};

export const useRunningAnalysis = () => {
  return useQuery({
    queryKey: ["running-analysis"],
    queryFn: fetchAnalysis,
    // [중요] 외부 API 연동 시 최적화 옵션
    // 1. 윈도우 포커스 시 재요청 방지 (API 호출 횟수 절약 및 2차 인증 이슈 방지)
    refetchOnWindowFocus: false, 
    // 2. 데이터 캐싱 시간: 10분 (러닝 데이터는 자주 변하지 않으므로)
    staleTime: 1000 * 60 * 10, 
    // 3. 에러 발생 시 재시도 횟수 제한 (인증 에러 등 무한 루프 방지)
    retry: 1, 
  });
};