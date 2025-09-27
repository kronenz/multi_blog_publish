# Tasks: Frontend SaaS Service

**Input**: Design documents from `/specs/002-frontend-saas-service/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → If not found: ERROR "No implementation plan found"
   → Extract: tech stack, libraries, structure
2. Load optional design documents:
   → data-model.md: Extract entities → model tasks
   → contracts/: Each file → contract test task
   → research.md: Extract decisions → setup tasks
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: models, services, CLI commands
   → Integration: DB, middleware, logging
   → Polish: unit tests, performance, docs
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests?
   → All entities have models?
   → All endpoints implemented?
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Web app**: `backend/src/`, `frontend/src/`

## Phase 3.1: Setup
- [x] T001 Create project structure (`backend` and `frontend` directories)
- [x] T002 Initialize Python project with FastAPI in the `backend` directory
- [x] T003 Initialize React project with TypeScript in the `frontend` directory
- [x] T004 [P] Configure linting and formatting tools for the backend
- [x] T005 [P] Configure linting and formatting tools for the frontend

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [x] T006 [P] Create contract tests for the User API endpoints in `backend/tests/contract/test_users.py`
- [x] T007 [P] Create contract tests for the KnowledgeVault API endpoints in `backend/tests/contract/test_knowledge_vaults.py`
- [x] T008 [P] Create contract tests for the BlogPost API endpoints in `backend/tests/contract/test_blog_posts.py`
- [x] T009 [P] Create integration test for user registration and authentication in `backend/tests/integration/test_auth.py`

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [x] T010 [P] Implement the User model in `backend/src/models/user.py`
- [x] T011 [P] Implement the KnowledgeVault model in `backend/src/models/knowledge_vault.py`
- [x] T012 [P] Implement the BlogPost model in `backend/src/models/blog_post.py`
- [x] T013 Implement the User service in `backend/src/services/user_service.py`
- [x] T014 Implement the KnowledgeVault service in `backend/src/services/knowledge_vault_service.py`
- [x] T015 Implement the BlogPost service in `backend/src/services/blog_post_service.py`
- [x] T016 Implement the User API endpoints in `backend/src/api/users.py`
- [x] T017 Implement the KnowledgeVault API endpoints in `backend/src/api/knowledge_vaults.py`
- [x] T018 Implement the BlogPost API endpoints in `backend/src/api/blog_posts.py`
- [x] T019 [BLOCKED] Implement the frontend components for user registration and login in `frontend/src/components/auth`
- [x] T020 [BLOCKED] Implement the frontend dashboard page in `frontend/src/pages/Dashboard.tsx`

## Phase 3.4: Integration
- [x] T021 Connect the backend services to the database
- [x] T022 [BLOCKED] Connect the frontend to the backend API

## Phase 3.5: Polish
- [x] T023 [P] Add unit tests for the backend services
- [x] T024 [P] [BLOCKED] Add unit tests for the frontend components
- [x] T025 [P] Update the API documentation

## Dependencies
- T001-T005 before T006-T025
- T006-T009 before T010-T022
- T010-T012 before T013-T015
- T013-T015 before T016-T018
- T016-T018 before T022
- T019-T020 before T022

## Parallel Example
```
# Launch T004 and T005 together:
Task: "Configure linting and formatting tools for the backend"
Task: "Configure linting and formatting tools for the frontend"
```
