# PR 동기화 가이드

Multi-Blog Publishing Platform의 PR(Pull Request) 발생 시 main 브랜치와 자동으로 동기화하는 방법을 안내합니다.

## 🚀 자동 동기화 기능

### 1. GitHub Actions 워크플로우

#### `sync-on-pr.yml`
- **트리거**: PR이 열리거나, 동기화되거나, 다시 열릴 때
- **기능**:
  - main 브랜치와 자동 병합
  - 충돌 자동 해결
  - 문서 검증
  - PR 설명 자동 업데이트
  - 동기화 완료 알림

#### `auto-merge.yml`
- **트리거**: PR이 열리거나, 동기화되거나, 다시 열릴 때
- **기능**:
  - PR이 main과 충돌하지 않는지 확인
  - 조건을 만족하면 자동으로 머지
  - Squash 머지 방식 사용

### 2. 로컬 동기화 도구

#### Bash 스크립트 (`scripts/sync-with-main.sh`)
```bash
# 기본 사용법
./scripts/sync-with-main.sh

# 또는 Git alias 사용
git sync-main
```

**주요 기능:**
- 현재 브랜치를 main과 자동 동기화
- 충돌 자동 해결 (README.md, gemini.md 우선)
- 변경사항 자동 스태시/복원
- 원격 저장소 자동 푸시
- 상세한 로그 출력

#### Python 도구 (`scripts/pr-sync-helper.py`)
```bash
# 기본 사용법
python3 scripts/pr-sync-helper.py

# 옵션들
python3 scripts/pr-sync-helper.py --help
python3 scripts/pr-sync-helper.py --status
python3 scripts/pr-sync-helper.py --no-auto-resolve
python3 scripts/pr-sync-helper.py --no-push
```

**주요 기능:**
- 고급 충돌 해결 로직
- JSON 형태의 상태 정보 출력
- 세밀한 제어 옵션
- 상세한 로그 및 에러 처리

## 📋 사용 시나리오

### 시나리오 1: 새로운 기능 브랜치에서 작업 중
```bash
# 1. 기능 브랜치 생성
git checkout -b feature/new-blog-platform

# 2. 작업 진행
# ... 코드 작성 ...

# 3. main 브랜치와 동기화 (충돌 발생 가능)
./scripts/sync-with-main.sh

# 4. PR 생성
git push origin feature/new-blog-platform
# GitHub에서 PR 생성
```

### 시나리오 2: PR이 이미 열린 상태에서 main이 업데이트됨
```bash
# 1. 현재 브랜치로 이동
git checkout your-feature-branch

# 2. 자동 동기화 실행
python3 scripts/pr-sync-helper.py

# 3. GitHub Actions가 자동으로 처리
# - main 브랜치와 병합
# - 충돌 해결
# - PR 설명 업데이트
# - 알림 댓글 추가
```

### 시나리오 3: 충돌이 발생한 경우
```bash
# 1. 동기화 시도
./scripts/sync-with-main.sh

# 2. 충돌 발생 시 자동 해결 시도
# - README.md: 현재 브랜치 우선
# - gemini.md: 현재 브랜치 우선
# - 기타 파일: 현재 브랜치 우선

# 3. 해결 후 자동 커밋 및 푸시
```

## ⚙️ 설정 및 커스터마이징

### Git 설정 (`.gitconfig`)
```ini
[alias]
    sync-main = !bash scripts/sync-with-main.sh
    sync = !git fetch origin && git merge origin/main
    update = !git fetch origin && git rebase origin/main
    conflicts = !git diff --name-only --diff-filter=U
    resolve = !git add . && git commit -m "chore: Resolve merge conflicts"
```

### 파일별 병합 전략 (`.gitattributes`)
```gitattributes
# 문서 파일들 - 병합 전략 설정
README.md merge=union
CHANGELOG.md merge=union
*.md merge=union

# 설정 파일들 - 병합 전략 설정
package.json merge=union
*.yml merge=union
*.yaml merge=union
```

### GitHub Actions 커스터마이징
워크플로우 파일을 수정하여 다음을 커스터마이징할 수 있습니다:
- 자동 머지 조건
- 충돌 해결 전략
- 알림 메시지
- 검증 규칙

## 🔧 문제 해결

### 자주 발생하는 문제들

#### 1. "작업 디렉토리에 커밋되지 않은 변경사항이 있습니다"
```bash
# 해결 방법 1: 변경사항 커밋
git add .
git commit -m "WIP: 작업 중인 변경사항"

# 해결 방법 2: 변경사항 스태시
git stash push -m "임시 저장"
```

#### 2. "main 브랜치 전환 실패"
```bash
# 현재 상태 확인
git status

# 충돌 해결 후 다시 시도
git add .
git commit -m "충돌 해결"
```

#### 3. "푸시 실패"
```bash
# 원격 저장소 확인
git remote -v

# SSH 키 확인
ssh -T git@github.com

# 강제 푸시 (주의!)
git push origin your-branch --force-with-lease
```

### 로그 확인
```bash
# 상세한 로그와 함께 실행
bash -x scripts/sync-with-main.sh

# Python 스크립트 상태 확인
python3 scripts/pr-sync-helper.py --status
```

## 📊 모니터링 및 알림

### GitHub Actions 로그
1. GitHub 저장소 → Actions 탭
2. 워크플로우 실행 기록 확인
3. 실패 시 상세 로그 확인

### PR 알림
- 동기화 완료 시 자동 댓글 추가
- 충돌 발생 시 해결 방법 안내
- 자동 머지 완료 시 알림

### 로컬 모니터링
```bash
# 브랜치 상태 확인
git status
git log --oneline -5

# main과의 차이 확인
git log --oneline main..HEAD
git log --oneline HEAD..main
```

## 🎯 베스트 프랙티스

### 1. 정기적인 동기화
```bash
# 작업 시작 전
git sync-main

# 작업 중간중간
git sync-main

# PR 생성 전
git sync-main
```

### 2. 충돌 예방
- 작은 단위로 자주 커밋
- main 브랜치 변경사항 정기 확인
- 팀원과 작업 영역 분리

### 3. 안전한 작업
- 중요한 변경사항은 백업
- 충돌 해결 후 테스트 실행
- PR 리뷰 요청 전 최종 동기화

## 🚨 주의사항

1. **자동 충돌 해결**: 현재 브랜치 우선으로 해결되므로, 중요한 변경사항이 손실될 수 있습니다.
2. **강제 푸시**: `--force-with-lease` 옵션을 사용하여 안전하게 푸시하세요.
3. **백업**: 중요한 작업 전에는 반드시 백업을 만드세요.
4. **테스트**: 동기화 후에는 반드시 테스트를 실행하세요.

---

이 가이드를 통해 PR 동기화를 효율적으로 관리하고, 팀 협업을 원활하게 진행할 수 있습니다! 🎉
