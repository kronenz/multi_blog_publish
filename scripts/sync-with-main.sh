#!/bin/bash

# Multi-Blog Publishing Platform - Main Branch Sync Script
# 이 스크립트는 현재 브랜치를 main 브랜치와 동기화합니다.

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

# 현재 브랜치 확인
CURRENT_BRANCH=$(git branch --show-current)
log_info "현재 브랜치: $CURRENT_BRANCH"

# main 브랜치인지 확인
if [ "$CURRENT_BRANCH" = "main" ]; then
    log_warning "현재 main 브랜치에 있습니다. 다른 브랜치로 전환해주세요."
    exit 1
fi

# 작업 디렉토리가 깨끗한지 확인
if ! git diff-index --quiet HEAD --; then
    log_warning "작업 디렉토리에 커밋되지 않은 변경사항이 있습니다."
    read -p "변경사항을 스태시하시겠습니까? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git stash push -m "Auto-stash before sync with main"
        log_info "변경사항을 스태시했습니다."
    else
        log_error "동기화를 취소합니다."
        exit 1
    fi
fi

# 원격 저장소에서 최신 정보 가져오기
log_info "원격 저장소에서 최신 정보를 가져오는 중..."
git fetch origin

# main 브랜치 업데이트
log_info "main 브랜치를 최신 상태로 업데이트하는 중..."
git checkout main
git pull origin main

# 원래 브랜치로 돌아가기
log_info "원래 브랜치($CURRENT_BRANCH)로 돌아가는 중..."
git checkout "$CURRENT_BRANCH"

# main 브랜치와 병합
log_info "main 브랜치와 병합하는 중..."
if git merge main --no-edit; then
    log_success "main 브랜치와 성공적으로 병합되었습니다."
else
    log_error "병합 중 충돌이 발생했습니다."
    
    # 충돌 파일 목록 표시
    log_info "충돌이 발생한 파일들:"
    git diff --name-only --diff-filter=U
    
    # 자동 충돌 해결 시도
    log_info "자동 충돌 해결을 시도합니다..."
    
    # README.md 충돌 해결 (우선순위: 현재 브랜치)
    if git status --porcelain | grep -q "README.md"; then
        log_info "README.md 충돌을 해결하는 중..."
        git checkout --ours README.md
        git add README.md
    fi
    
    # gemini.md 충돌 해결
    if git status --porcelain | grep -q "gemini.md"; then
        log_info "gemini.md 충돌을 해결하는 중..."
        git checkout --ours gemini.md
        git add gemini.md
    fi
    
    # 기타 충돌 파일들 처리
    for file in $(git diff --name-only --diff-filter=U); do
        log_info "$file 충돌을 해결하는 중..."
        git checkout --ours "$file"
        git add "$file"
    done
    
    # 충돌 해결 후 커밋
    if git diff --staged --quiet; then
        log_info "충돌 해결 후 변경사항이 없습니다."
    else
        git commit -m "chore: Auto-resolve merge conflicts with main branch

        - Automatically merged changes from main branch
        - Resolved merge conflicts in documentation and config files
        - Updated project files to maintain consistency"
        log_success "충돌 해결이 완료되었습니다."
    fi
fi

# 스태시된 변경사항 복원
if git stash list | grep -q "Auto-stash before sync with main"; then
    log_info "스태시된 변경사항을 복원하는 중..."
    git stash pop
    log_success "스태시된 변경사항이 복원되었습니다."
fi

# 원격 저장소에 푸시
log_info "변경사항을 원격 저장소에 푸시하는 중..."
if git push origin "$CURRENT_BRANCH"; then
    log_success "원격 저장소에 성공적으로 푸시되었습니다."
else
    log_error "푸시에 실패했습니다. 수동으로 푸시해주세요."
    exit 1
fi

# 최종 상태 확인
log_info "동기화 완료! 현재 상태:"
echo "  - 현재 브랜치: $(git branch --show-current)"
echo "  - 최신 커밋: $(git log --oneline -1)"
echo "  - main 브랜치와의 차이: $(git rev-list --count main..HEAD) 커밋 앞서있음"

log_success "main 브랜치와의 동기화가 완료되었습니다! 🎉"
