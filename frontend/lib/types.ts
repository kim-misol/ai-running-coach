// lib/types.ts

export interface RacePrediction {
  distance_km: number;
  predicted_time_str: string;
  confidence_score: number;
}

export interface CoachFeedback {
  summary: string;
  strength: string[];
  weakness: string[];
  suggested_workout: string;
  race_predictions: RacePrediction[];
}

export interface RunningMetrics {
  distance_meters: number;
  duration_seconds: number;
  average_heart_rate: number;
  max_heart_rate: number;
  calories: number;
  avg_pace: number; // 분/km
  activity_date: string;
}

// API 응답 전체 타입 (필요시 확장)
export interface AnalysisResponse extends CoachFeedback {
  metrics: RunningMetrics; // UI 편의를 위해 합쳐서 관리한다고 가정
  chart_data: TimeSeriesDataPoint[]; // <-- 추가됨
}

export interface TimeSeriesDataPoint {
  time_offset: number; // 시작부터 지난 시간(초)
  heart_rate: number;
  pace: number; // 분/km (decimal)
  elevation?: number;
}
