// frontend/__tests__/Dashboard.test.tsx
import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/react'
import Page from '@/app/page' // QueryProvider가 감싸진 Page 컴포넌트

// useRunningData 훅 Mocking
jest.mock('@/hooks/useRunningData', () => ({
  useRunningAnalysis: jest.fn()
}))

import { useRunningAnalysis } from '@/hooks/useRunningData'

describe('Dashboard Page', () => {
  it('renders loading state initially', () => {
    (useRunningAnalysis as jest.Mock).mockReturnValue({
      isLoading: true,
      data: null
    })

    render(<Page />)
    expect(screen.getByText('Analyzing your run...')).toBeInTheDocument()
  })

  it('renders dashboard with data successfully', () => {
    (useRunningAnalysis as jest.Mock).mockReturnValue({
      isLoading: false,
      isError: false,
      data: {
        metrics: {
          distance_meters: 5000,
          duration_seconds: 1500,
          average_heart_rate: 150,
          max_heart_rate: 180,
          avg_pace: 5.0,
          activity_date: "2024-01-01",
          calories: 500
        },
        summary: "Good job!",
        strength: ["Pace"],
        weakness: ["None"],
        suggested_workout: "Rest",
        race_predictions: [],
        chart_data: []
      }
    })

    render(<Page />)
    
    // 주요 텍스트가 화면에 나오는지 확인
    expect(screen.getByText('Training Dashboard')).toBeInTheDocument()
    expect(screen.getByText('5.00')).toBeInTheDocument() // Distance (km)
    expect(screen.getByText('150')).toBeInTheDocument() // Heart Rate
  })

  it('renders error state', () => {
    (useRunningAnalysis as jest.Mock).mockReturnValue({
      isLoading: false,
      isError: true,
      data: null
    })

    render(<Page />)
    expect(screen.getByText('Failed to load data.')).toBeInTheDocument()
  })
})