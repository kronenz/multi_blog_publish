# 🚀 Multi-Blog Publishing Platform 배포 가이드

## 📋 배포 방법

### 방법 1: 스크립트를 사용한 배포 (권장)

```bash
# 1. 프로젝트 클론
git clone https://github.com/kronenz/multi_blog_publish.git
cd multi_blog_publish

# 2. 실행 권한 부여
chmod +x deploy.sh

# 3. 전체 애플리케이션 배포
./deploy.sh all

# 4. 상태 확인
./deploy.sh status

# 5. 프로세스 종료
./deploy.sh stop
```

### 방법 2: Docker를 사용한 배포

```bash
# 1. 프로젝트 클론
git clone https://github.com/kronenz/multi_blog_publish.git
cd multi_blog_publish

# 2. Docker Compose로 전체 스택 실행
docker-compose up -d

# 3. 로그 확인
docker-compose logs -f

# 4. 서비스 중지
docker-compose down
```

### 방법 3: 수동 배포

#### 백엔드 배포

```bash
# 1. 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

# 2. 의존성 설치
pip install --upgrade pip
pip install fastapi uvicorn

# 3. 백엔드 서버 실행
uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload
```

#### 프론트엔드 배포

```bash
# 1. 프론트엔드 디렉토리로 이동
cd frontend

# 2. 의존성 설치
npm install

# 3. 빌드
REACT_APP_API_BASE_URL=http://localhost:8001 npm run build

# 4. 정적 파일 서빙
npx serve -s build -l 3001
```

## 🔧 환경 요구사항

### 시스템 요구사항
- **OS**: Linux, macOS, Windows
- **Python**: 3.11+
- **Node.js**: 18+
- **npm**: 9+

### 포트 요구사항
- **백엔드**: 8001
- **프론트엔드**: 3001

## 🐛 문제 해결

### 1. package.json을 찾을 수 없는 오류

```bash
# 오류: Could not read package.json: Error: ENOENT: no such file or directory

# 해결책:
# 1. 올바른 디렉토리인지 확인
pwd
ls -la

# 2. frontend 디렉토리로 이동
cd frontend
ls -la package.json

# 3. 프로젝트 구조 확인
cd ..
find . -name "package.json" -type f
```

### 2. EMFILE 오류 (파일 디스크립터 제한)

```bash
# 오류: Error: EMFILE: too many open files

# 해결책:
# 1. 파일 디스크립터 제한 확인
ulimit -n

# 2. 제한 증가 (임시)
ulimit -n 65536

# 3. 또는 정적 빌드 사용
cd frontend
npm run build
npx serve -s build -l 3001
```

### 3. 포트 충돌 오류

```bash
# 오류: Address already in use

# 해결책:
# 1. 포트 사용 확인
netstat -tlnp | grep -E "(8001|3001)"

# 2. 프로세스 종료
pkill -f uvicorn
pkill -f "serve.*3001"

# 3. 다른 포트 사용
uvicorn backend.main:app --host 0.0.0.0 --port 8002
npx serve -s build -l 3002
```

### 4. CORS 오류

```bash
# 오류: CORS policy: No 'Access-Control-Allow-Origin' header

# 해결책:
# 1. 백엔드 CORS 설정 확인
cat backend/main.py | grep -A 10 CORSMiddleware

# 2. 프론트엔드 API URL 확인
echo $REACT_APP_API_BASE_URL
```

## 📊 모니터링

### 프로세스 확인

```bash
# 실행 중인 프로세스 확인
ps aux | grep -E "(uvicorn|serve)" | grep -v grep

# 포트 사용 현황
netstat -tlnp | grep -E "(8001|3001)"

# 메모리 사용량
free -h
```

### 로그 확인

```bash
# 백엔드 로그
tail -f backend.log

# 프론트엔드 로그
tail -f frontend.log

# Docker 로그
docker-compose logs -f
```

### 헬스 체크

```bash
# 백엔드 헬스 체크
curl http://localhost:8001/health

# 프론트엔드 헬스 체크
curl http://localhost:3001

# API 문서 확인
curl http://localhost:8001/docs
```

## 🔄 업데이트

### 코드 업데이트

```bash
# 1. 최신 코드 가져오기
git pull origin main

# 2. 의존성 업데이트
pip install -r requirements.txt
cd frontend && npm install

# 3. 서비스 재시작
./deploy.sh stop
./deploy.sh all
```

### Docker 업데이트

```bash
# 1. 최신 코드 가져오기
git pull origin main

# 2. 이미지 재빌드
docker-compose build --no-cache

# 3. 서비스 재시작
docker-compose down
docker-compose up -d
```

## 📝 환경 변수

### 백엔드 환경 변수

```bash
# .env 파일 생성
cat > .env << EOF
API_HOST=0.0.0.0
API_PORT=8001
DEBUG=True
EOF
```

### 프론트엔드 환경 변수

```bash
# .env 파일 생성
cat > frontend/.env << EOF
REACT_APP_API_BASE_URL=http://localhost:8001
REACT_APP_API_TIMEOUT=10000
EOF
```

## 🚨 보안 고려사항

1. **방화벽 설정**: 필요한 포트만 열기
2. **HTTPS 사용**: 프로덕션에서는 SSL 인증서 사용
3. **환경 변수 보호**: 민감한 정보는 환경 변수로 관리
4. **정기 업데이트**: 의존성 패키지 정기 업데이트

## 📞 지원

문제가 발생하면 다음을 확인하세요:

1. **로그 파일**: `backend.log`, `frontend.log`
2. **시스템 리소스**: 메모리, 디스크 공간
3. **네트워크 연결**: 포트 접근 가능성
4. **의존성 버전**: Python, Node.js 버전 호환성

---

**배포 성공 시 접속 URL:**
- 🌐 웹 애플리케이션: http://localhost:3001
- 🔧 API 서버: http://localhost:8001
- 📚 API 문서: http://localhost:8001/docs
