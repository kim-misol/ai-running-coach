import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/react'
import Page from '@/app/page' // QueryProvider 포함된 최상위 컴포넌트
import { useRunningAnalysis } from '@/hooks/useRunningData'

// 1. Mock the module
jest.mock('@/hooks/useRunningData', () => ({
  useRunningAnalysis: jest.fn()
}))

// 2. Create a typed mock helper
const mockUseRunningAnalysis = useRunningAnalysis as jest.MockedFunction<typeof useRunningAnalysis>


describe('Dashboard Page', () => {
  it('renders loading state initially', () => {
    // 3. Use the typed mock
    mockUseRunningAnalysis.mockReturnValue({
      isLoading: true,
      data: undefined,
      isError: false 
    } as any)

    render(<Page />)
    expect(screen.getByText('Analyzing your run...')).toBeInTheDocument()
  })

  it('renders dashboard with data successfully', () => {
    mockUseRunningAnalysis.mockReturnValue({
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
    } as any)

    render(<Page />)
    
    // 주요 텍스트가 화면에 나오는지 확인
    expect(screen.getByText('Training Dashboard')).toBeInTheDocument()
    expect(screen.getByText('5.00')).toBeInTheDocument() // Distance (km)
    expect(screen.getByText('150')).toBeInTheDocument() // Heart Rate
  })

  it('renders error state', () => {
    mockUseRunningAnalysis.mockReturnValue({
      isLoading: false,
      isError: true,
      data: undefined
    } as any)

    render(<Page />)
    expect(screen.getByText('Failed to load data.')).toBeInTheDocument()
  })
})