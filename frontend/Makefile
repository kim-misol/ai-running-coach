.PHONY: install dev build start lint type-check clean

PM = npm

install:
	@echo "📦 Installing frontend dependencies..."
	$(PM) install

dev:
	@echo "🚀 Starting frontend development server..."
	$(PM) run dev

build:
	@echo "🏗 Building frontend for production..."
	$(PM) run build

start:
	@echo "🏃 Starting production server..."
	$(PM) run start

lint:
	@echo "🔍 Running Linter..."
	$(PM) run lint

type-check:
	@echo "✅ Running TypeScript Type Checker..."
	# tsc --noEmit은 컴파일 파일 생성 없이 타입 오류만 검사합니다.
	$(PM) exec tsc -- --noEmit

test:
	@echo "🧪 Running Tests..."
	# 테스트 스크립트가 있다면 실행 (현재는 echo만)
	@echo "No tests specified yet."

clean:
	@echo "🧹 Cleaning cache..."
	rm -rf .next node_modules package-lock.json