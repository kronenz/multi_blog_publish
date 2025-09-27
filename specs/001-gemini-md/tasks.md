# Tasks: Gemini Integration

**Input**: Design documents from `/specs/001-gemini-md/`
**Prerequisites**: plan.md (required)

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
- **Single project**: `src/`, `tests/` at repository root

## Phase 3.1: Setup
- [x] T001 Add `google-generativeai` to `requirements.txt`

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [x] T002 [P] Create integration test for Gemini API connection in `tests/integration/test_gemini_api.py`
- [x] T003 [P] Create unit tests for Gemini configuration in `tests/unit/test_gemini_config.py`

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [x] T004 Create `GeminiConfiguration` model in `src/models/gemini_config.py`
- [x] T005 Create a service to manage Gemini API calls in `src/services/gemini_service.py`
- [ ] T006 [BLOCKED] Add "Gemini" to the list of AI providers in the UI
- [ ] T007 [BLOCKED] Implement the UI for selecting Gemini and generating content

## Phase 3.4: Integration
- [ ] T008 [BLOCKED] Integrate the `GeminiService` with the UI
- [x] T009 Implement secure storage and retrieval of the Gemini API key

## Phase 3.5: Polish
- [x] T010 [P] Add documentation for the Gemini integration in `docs/gemini_integration.md`
- [x] T011 [P] Add logging for Gemini API requests

## Dependencies
- T001 before T002, T003, T004, T005
- T002, T003 before T004, T005
- T004, T005 before T008
- T006, T007 before T008

## Parallel Example
```
# Launch T002 and T003 together:
Task: "Create integration test for Gemini API connection in tests/integration/test_gemini_api.py"
Task: "Create unit tests for Gemini configuration in tests/unit/test_gemini_config.py"
```
