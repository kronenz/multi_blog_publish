#!/usr/bin/env python3
"""
Multi-Blog Publishing Platform - PR Sync Helper
PR 발생 시 자동으로 main 브랜치와 동기화하는 도구
"""

import os
import sys
import subprocess
import json
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class PRSyncHelper:
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
        self.colors = {
            'RED': '\033[0;31m',
            'GREEN': '\033[0;32m',
            'YELLOW': '\033[1;33m',
            'BLUE': '\033[0;34m',
            'NC': '\033[0m'  # No Color
        }
    
    def log(self, message: str, level: str = "INFO"):
        """로그 메시지 출력"""
        color = self.colors.get(level, self.colors['NC'])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{color}[{level}] {timestamp} - {message}{self.colors['NC']}")
    
    def run_command(self, command: str, check: bool = True) -> Tuple[int, str, str]:
        """명령어 실행"""
        try:
            result = subprocess.run(
                command.split(),
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=check
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return e.returncode, e.stdout, e.stderr
    
    def get_current_branch(self) -> str:
        """현재 브랜치 이름 반환"""
        _, stdout, _ = self.run_command("git branch --show-current")
        return stdout.strip()
    
    def get_branch_status(self) -> Dict[str, any]:
        """브랜치 상태 정보 반환"""
        status = {
            'current_branch': self.get_current_branch(),
            'is_clean': False,
            'ahead_of_main': 0,
            'behind_main': 0,
            'has_conflicts': False
        }
        
        # 작업 디렉토리 상태 확인
        _, stdout, _ = self.run_command("git status --porcelain")
        status['is_clean'] = len(stdout.strip()) == 0
        
        # main 브랜치와의 차이 확인
        try:
            _, stdout, _ = self.run_command("git rev-list --count main..HEAD")
            status['ahead_of_main'] = int(stdout.strip()) if stdout.strip() else 0
        except:
            status['ahead_of_main'] = 0
        
        try:
            _, stdout, _ = self.run_command("git rev-list --count HEAD..main")
            status['behind_main'] = int(stdout.strip()) if stdout.strip() else 0
        except:
            status['behind_main'] = 0
        
        return status
    
    def sync_with_main(self, auto_resolve: bool = True) -> bool:
        """main 브랜치와 동기화"""
        self.log("main 브랜치와 동기화를 시작합니다...")
        
        # 1. 원격 저장소에서 최신 정보 가져오기
        self.log("원격 저장소에서 최신 정보를 가져오는 중...")
        returncode, stdout, stderr = self.run_command("git fetch origin")
        if returncode != 0:
            self.log(f"fetch 실패: {stderr}", "ERROR")
            return False
        
        # 2. main 브랜치 업데이트
        self.log("main 브랜치를 최신 상태로 업데이트하는 중...")
        current_branch = self.get_current_branch()
        
        returncode, stdout, stderr = self.run_command("git checkout main")
        if returncode != 0:
            self.log(f"main 브랜치 전환 실패: {stderr}", "ERROR")
            return False
        
        returncode, stdout, stderr = self.run_command("git pull origin main")
        if returncode != 0:
            self.log(f"main 브랜치 업데이트 실패: {stderr}", "ERROR")
            return False
        
        # 3. 원래 브랜치로 돌아가기
        self.log(f"원래 브랜치({current_branch})로 돌아가는 중...")
        returncode, stdout, stderr = self.run_command(f"git checkout {current_branch}")
        if returncode != 0:
            self.log(f"브랜치 전환 실패: {stderr}", "ERROR")
            return False
        
        # 4. main 브랜치와 병합
        self.log("main 브랜치와 병합하는 중...")
        returncode, stdout, stderr = self.run_command("git merge main --no-edit", check=False)
        
        if returncode == 0:
            self.log("main 브랜치와 성공적으로 병합되었습니다.", "SUCCESS")
            return True
        else:
            self.log("병합 중 충돌이 발생했습니다.", "WARNING")
            
            if auto_resolve:
                return self.auto_resolve_conflicts()
            else:
                self.log("수동으로 충돌을 해결해주세요.", "ERROR")
                return False
    
    def auto_resolve_conflicts(self) -> bool:
        """충돌 자동 해결"""
        self.log("자동 충돌 해결을 시도합니다...")
        
        # 충돌 파일 목록 가져오기
        _, stdout, _ = self.run_command("git diff --name-only --diff-filter=U")
        conflict_files = stdout.strip().split('\n') if stdout.strip() else []
        
        if not conflict_files:
            self.log("충돌 파일이 없습니다.", "WARNING")
            return True
        
        self.log(f"충돌 파일들: {', '.join(conflict_files)}")
        
        # 파일별 충돌 해결
        resolved_files = []
        for file in conflict_files:
            if not file:
                continue
                
            self.log(f"{file} 충돌을 해결하는 중...")
            
            # 우선순위: 현재 브랜치 (--ours)
            returncode, stdout, stderr = self.run_command(f"git checkout --ours {file}", check=False)
            if returncode == 0:
                self.run_command(f"git add {file}")
                resolved_files.append(file)
                self.log(f"{file} 충돌 해결 완료", "SUCCESS")
            else:
                self.log(f"{file} 충돌 해결 실패: {stderr}", "ERROR")
        
        if resolved_files:
            # 충돌 해결 후 커밋
            commit_message = f"""chore: Auto-resolve merge conflicts with main branch

- Automatically merged changes from main branch
- Resolved conflicts in: {', '.join(resolved_files)}
- Updated project files to maintain consistency

Generated by PR Sync Helper at {datetime.now().isoformat()}"""
            
            returncode, stdout, stderr = self.run_command(f'git commit -m "{commit_message}"', check=False)
            if returncode == 0:
                self.log("충돌 해결이 완료되었습니다.", "SUCCESS")
                return True
            else:
                self.log(f"커밋 실패: {stderr}", "ERROR")
                return False
        else:
            self.log("해결된 충돌이 없습니다.", "WARNING")
            return True
    
    def push_changes(self) -> bool:
        """변경사항 푸시"""
        current_branch = self.get_current_branch()
        self.log(f"변경사항을 원격 저장소에 푸시하는 중... (브랜치: {current_branch})")
        
        returncode, stdout, stderr = self.run_command(f"git push origin {current_branch}")
        if returncode == 0:
            self.log("원격 저장소에 성공적으로 푸시되었습니다.", "SUCCESS")
            return True
        else:
            self.log(f"푸시 실패: {stderr}", "ERROR")
            return False
    
    def create_pr_info(self) -> Dict[str, any]:
        """PR 정보 생성"""
        status = self.get_branch_status()
        
        pr_info = {
            'branch': status['current_branch'],
            'is_clean': status['is_clean'],
            'ahead_of_main': status['ahead_of_main'],
            'behind_main': status['behind_main'],
            'sync_timestamp': datetime.now().isoformat(),
            'ready_for_merge': status['is_clean'] and status['behind_main'] == 0
        }
        
        return pr_info
    
    def run_sync(self, auto_resolve: bool = True, push: bool = True) -> bool:
        """전체 동기화 프로세스 실행"""
        self.log("=== PR 동기화 프로세스 시작 ===")
        
        # 현재 상태 확인
        status = self.get_branch_status()
        self.log(f"현재 브랜치: {status['current_branch']}")
        self.log(f"작업 디렉토리 상태: {'깨끗함' if status['is_clean'] else '변경사항 있음'}")
        self.log(f"main 브랜치보다 앞서있음: {status['ahead_of_main']} 커밋")
        self.log(f"main 브랜치보다 뒤처짐: {status['behind_main']} 커밋")
        
        if status['current_branch'] == 'main':
            self.log("현재 main 브랜치에 있습니다. 다른 브랜치로 전환해주세요.", "ERROR")
            return False
        
        # 동기화 실행
        if not self.sync_with_main(auto_resolve):
            return False
        
        # 푸시 (옵션)
        if push:
            if not self.push_changes():
                return False
        
        # 최종 상태 출력
        final_status = self.get_branch_status()
        self.log("=== 동기화 완료 ===")
        self.log(f"현재 브랜치: {final_status['current_branch']}")
        self.log(f"main 브랜치와의 차이: {final_status['ahead_of_main']} 커밋 앞서있음")
        self.log("PR이 이제 main 브랜치와 동기화되었습니다! 🎉", "SUCCESS")
        
        return True

def main():
    parser = argparse.ArgumentParser(description='PR Sync Helper - main 브랜치와 자동 동기화')
    parser.add_argument('--repo-path', default='.', help='저장소 경로 (기본값: 현재 디렉토리)')
    parser.add_argument('--no-auto-resolve', action='store_true', help='자동 충돌 해결 비활성화')
    parser.add_argument('--no-push', action='store_true', help='푸시 비활성화')
    parser.add_argument('--status', action='store_true', help='현재 상태만 확인')
    
    args = parser.parse_args()
    
    helper = PRSyncHelper(args.repo_path)
    
    if args.status:
        status = helper.get_branch_status()
        print(json.dumps(status, indent=2, ensure_ascii=False))
        return
    
    success = helper.run_sync(
        auto_resolve=not args.no_auto_resolve,
        push=not args.no_push
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
