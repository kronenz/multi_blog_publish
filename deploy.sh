#!/bin/bash

# Multi-Blog Publishing Platform 배포 스크립트
# 사용법: ./deploy.sh [backend|frontend|all]

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 로그 함수
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 프로젝트 루트 디렉토리 확인
if [ ! -f "README.md" ]; then
    log_error "프로젝트 루트 디렉토리가 아닙니다. README.md 파일이 없습니다."
    exit 1
fi

# 백엔드 배포
deploy_backend() {
    log_info "백엔드 배포 시작..."
    
    # 가상환경 생성 및 활성화
    if [ ! -d "venv" ]; then
        log_info "Python 가상환경 생성 중..."
        python3 -m venv venv
    fi
    
    log_info "가상환경 활성화 중..."
    source venv/bin/activate
    
    # pip 업그레이드
    log_info "pip 업그레이드 중..."
    pip install --upgrade pip
    
    # 의존성 설치
    log_info "백엔드 의존성 설치 중..."
    pip install fastapi uvicorn
    
    # 백엔드 서버 실행
    log_info "백엔드 서버 시작 중... (포트 8001)"
    log_warning "백엔드는 백그라운드에서 실행됩니다."
    nohup uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload > backend.log 2>&1 &
    
    # 서버 시작 대기
    sleep 3
    
    # 헬스 체크
    if curl -s http://localhost:8001/health > /dev/null; then
        log_success "백엔드 서버가 성공적으로 시작되었습니다!"
        log_info "API 문서: http://localhost:8001/docs"
        log_info "헬스 체크: http://localhost:8001/health"
    else
        log_error "백엔드 서버 시작에 실패했습니다. 로그를 확인하세요: cat backend.log"
        exit 1
    fi
}

# 프론트엔드 배포
deploy_frontend() {
    log_info "프론트엔드 배포 시작..."
    
    # 프론트엔드 디렉토리 확인
    if [ ! -f "frontend/package.json" ]; then
        log_error "frontend/package.json 파일을 찾을 수 없습니다."
        exit 1
    fi
    
    cd frontend
    
    # Node.js 버전 확인
    log_info "Node.js 버전 확인 중..."
    node --version
    npm --version
    
    # 의존성 설치
    log_info "프론트엔드 의존성 설치 중..."
    npm install
    
    # 빌드
    log_info "프론트엔드 빌드 중..."
    REACT_APP_API_BASE_URL=http://localhost:8001 npm run build
    
    # 정적 파일 서빙
    log_info "프론트엔드 서버 시작 중... (포트 3001)"
    log_warning "프론트엔드는 백그라운드에서 실행됩니다."
    nohup npx serve -s build -l 3001 > ../frontend.log 2>&1 &
    
    # 서버 시작 대기
    sleep 3
    
    # 서버 상태 확인
    if curl -s http://localhost:3001 > /dev/null; then
        log_success "프론트엔드 서버가 성공적으로 시작되었습니다!"
        log_info "웹 애플리케이션: http://localhost:3001"
    else
        log_error "프론트엔드 서버 시작에 실패했습니다. 로그를 확인하세요: cat frontend.log"
        exit 1
    fi
    
    cd ..
}

# 전체 배포
deploy_all() {
    log_info "전체 애플리케이션 배포 시작..."
    deploy_backend
    deploy_frontend
    
    log_success "전체 배포가 완료되었습니다!"
    log_info "백엔드: http://localhost:8001"
    log_info "프론트엔드: http://localhost:3001"
    log_info "API 문서: http://localhost:8001/docs"
}

# 프로세스 확인
check_processes() {
    log_info "실행 중인 프로세스 확인..."
    echo "=== 백엔드 프로세스 ==="
    ps aux | grep uvicorn | grep -v grep || echo "백엔드 프로세스가 실행되지 않았습니다."
    echo "=== 프론트엔드 프로세스 ==="
    ps aux | grep serve | grep -v grep || echo "프론트엔드 프로세스가 실행되지 않았습니다."
    echo "=== 포트 사용 현황 ==="
    netstat -tlnp | grep -E "(8001|3001)" || echo "사용 중인 포트가 없습니다."
}

# 프로세스 종료
stop_all() {
    log_info "모든 프로세스 종료 중..."
    pkill -f uvicorn || true
    pkill -f "serve.*3001" || true
    log_success "모든 프로세스가 종료되었습니다."
}

# 메인 로직
case "${1:-all}" in
    "backend")
        deploy_backend
        ;;
    "frontend")
        deploy_frontend
        ;;
    "all")
        deploy_all
        ;;
    "status")
        check_processes
        ;;
    "stop")
        stop_all
        ;;
    "help"|"-h"|"--help")
        echo "사용법: $0 [backend|frontend|all|status|stop|help]"
        echo ""
        echo "명령어:"
        echo "  backend   - 백엔드만 배포"
        echo "  frontend  - 프론트엔드만 배포"
        echo "  all       - 전체 애플리케이션 배포 (기본값)"
        echo "  status    - 실행 중인 프로세스 확인"
        echo "  stop      - 모든 프로세스 종료"
        echo "  help      - 도움말 표시"
        ;;
    *)
        log_error "알 수 없는 명령어: $1"
        echo "사용법: $0 [backend|frontend|all|status|stop|help]"
        exit 1
        ;;
esac
