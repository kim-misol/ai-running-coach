# AI Running Coach 🏃‍♂️🤖

Garmin 데이터를 활용하여 개인화된 러닝 코칭과 레이스 예측을 제공하는 서비스입니다.

## 🌟 Features
- **Garmin Integration**: 가민 커넥트 활동 데이터 자동 동기화
- **AI Analysis**: 훈련 데이터 기반 강점/약점 분석 (Powered by LLM)
- **Race Prediction**: 현재 퍼포먼스 기반 5k, 10k, 하프, 풀코스 기록 예측
- **Workout Suggestion**: 맞춤형 다음 훈련 스케줄 제안

## 🛠 Tech Stack
- **Backend**: Python 3.10+, FastAPI, Pydantic, GarminConnect, LangChain
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **DevOps**: Docker, Poetry, Ruff, GitHub Actions

## 🚀 Getting Started

### Backend
1. 의존성 설치
    ```bash
    cd backend
    make install
    ```
    
2. 서버 실행
    ```bash
    make run
    ```
    Docs available at: `http://localhost:8000/docs`

### Frontend
(추후 추가 예정)
   ```bash
    cd frontend
    make install
    # 패키지 버전 지정
    # npm install --legacy-peer-deps
    npm install -D typescript @types/node @types/react @types/react-dom
    make type-check
    ```

## Project Structure

```Plaintext
ai-running-coach/
├── .gitignore                # Git 무시 파일 목록
├── README.md                 # 프로젝트 설명
├── fix_node_compatibility.py # (방금 실행한 스크립트 - 삭제 가능)
├── setup_*.py                # (이전에 실행한 설정 스크립트들 - 삭제 가능)
│
├── .github/
│   └── workflows/
│       └── frontend-ci.yml   # GitHub Actions 설정 (CI)
│
├── backend/                  # Python FastAPI Backend
│   ├── Makefile              # 백엔드 실행/테스트 명령어
│   ├── pyproject.toml        # 의존성 및 툴 설정 (Ruff 등)
│   └── app/
│       ├── __init__.py
│       ├── main.py           # FastAPI 진입점
│       ├── models.py         # Pydantic 데이터 모델
│       ├── core/
│       │   ├── __init__.py
│       │   └── config.py     # 환경변수 설정
│       └── services/
│           ├── __init__.py
│           ├── ai_coach.py   # AI 로직 (Mock)
│           └── garmin_service.py # 가민 연동 로직 (Mock)
│
└── frontend/                 # Next.js 14 Frontend
    ├── Makefile              # 프론트엔드 실행 명령어 (dev, build, lint 등)
    ├── package.json          # Node v18 호환 설정 (Next.js 14)
    ├── package-lock.json     # 의존성 잠금 파일
    ├── tsconfig.json         # TypeScript 설정
    ├── next-env.d.ts         # Next.js 타입 정의
    ├── tailwind.config.ts    # Tailwind CSS 설정
    ├── postcss.config.js     # PostCSS 설정
    │
    ├── node_modules/         # (npm install로 생성된 폴더)
    │
    ├── app/                  # App Router
    │   ├── globals.css       # 전역 스타일 (Tailwind directives)
    │   ├── layout.tsx        # 루트 레이아웃
    │   └── page.tsx          # 대시보드 메인 페이지
    │
    ├── components/
    │   ├── analysis/
    │   │   ├── AIReport.tsx  # AI 분석 텍스트 UI
    │   │   └── RunChart.tsx  # [추가됨] Recharts 그래프 컴포넌트
    │   └── metrics/
    │       └── StatCard.tsx  # 통계 카드 UI
    │
    ├── hooks/
    │   └── useRunningData.ts # React Query 데이터 페칭 훅
    │
    └── lib/
        ├── types.ts          # TypeScript 인터페이스
        └── utils.ts          # 포맷팅 유틸리티 함수
```