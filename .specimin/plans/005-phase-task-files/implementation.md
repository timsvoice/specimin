# Implementation Tasks: Phase-Based Task File Generation

**Overview**: Extend the `/specimin:cmd.implement` command to automatically generate phase-specific markdown files and a JSON manifest from implementation.md, enabling coding agents to work through focused task chunks with programmatic status tracking.

**Total Tasks**: 20
**Phases**: 6
**Estimated Completion**: 2-3 hours (primarily prompt engineering and manual testing)

---

## Phase 1: Foundation - Task Directory Setup

**Dependencies**: None
**Parallel Opportunities**: 0

- [ ] T001 Add Stage 7 section "Generate Phase Files and Manifest" after Stage 6 in .claude-plugin/commands/cmd.implement.md (AC1)
- [ ] T002 Add instruction to create `.specimin/plans/{branch}/tasks/` directory using Bash mkdir command in .claude-plugin/commands/cmd.implement.md (AC1)

---

## Phase 2: Implementation Parsing Logic

**Dependencies**: Phase 1 complete
**Parallel Opportunities**: 0

- [ ] T003 Add prompt instruction to read implementation.md and identify phase boundaries (headers like `## Phase N:`) in .claude-plugin/commands/cmd.implement.md (AC2)
- [ ] T004 Add prompt instruction to extract task data (task ID, description, phase number) from checkbox lines in .claude-plugin/commands/cmd.implement.md (AC2, AC3)
- [ ] T005 Add prompt instruction to store extracted data in structured format (phase → tasks mapping) in .claude-plugin/commands/cmd.implement.md (AC2)

---

## Phase 3: Phase File Generation

**Dependencies**: Phase 2 complete
**Parallel Opportunities**: 0

- [ ] T006 Add prompt instruction to create phase_N.md files using Write tool with numeric naming in .claude-plugin/commands/cmd.implement.md (AC1, AC2)
- [ ] T007 Add prompt instruction to include phase header (name from implementation.md) in each phase file in .claude-plugin/commands/cmd.implement.md (AC2)
- [ ] T008 Add prompt instruction to copy phase metadata (dependencies, parallel opportunities) into phase files in .claude-plugin/commands/cmd.implement.md (AC2)
- [ ] T009 Add prompt instruction to write filtered task list (preserving original task IDs) to each phase file in .claude-plugin/commands/cmd.implement.md (AC2)

---

## Phase 4: Manifest Generation

**Dependencies**: Phase 2 complete
**Parallel Opportunities**: 4 (entire phase can run parallel with Phase 3)

- [ ] T010 [P] Add prompt instruction to construct JSON array of task objects with schema: {id, description, phase, status} in .claude-plugin/commands/cmd.implement.md (AC3)
- [ ] T011 [P] Add prompt instruction with JSON escaping examples (quotes, backslashes, newlines) in .claude-plugin/commands/cmd.implement.md (AC3, EC3)
- [ ] T012 [P] Add prompt instruction to initialize all task status fields to "pending" in .claude-plugin/commands/cmd.implement.md (AC3)
- [ ] T013 [P] Add prompt instruction to write manifest.json using Write tool to tasks directory in .claude-plugin/commands/cmd.implement.md (AC3)

---

## Phase 5: Edge Case Handling

**Dependencies**: Phase 3 and Phase 4 complete
**Parallel Opportunities**: 3

- [ ] T014 [P] Add conditional logic to handle single-phase implementations (still create phase_1.md) in .claude-plugin/commands/cmd.implement.md (EC1)
- [ ] T015 [P] Add logic to skip file creation for empty phases but note in manifest in .claude-plugin/commands/cmd.implement.md (EC2)
- [ ] T016 [P] Add validation step to count detected phases and show error if 0 phases found in .claude-plugin/commands/cmd.implement.md (Risk1)

---

## Phase 6: Workflow Integration and Verification

**Dependencies**: Phase 5 complete
**Parallel Opportunities**: 0

- [ ] T017 Update Stage 6 "Save Approved Tasks" to trigger Stage 7 after writing implementation.md in .claude-plugin/commands/cmd.implement.md (AC1)
- [ ] T018 Add confirmation message showing "Generated N phase files and manifest with M tasks" in .claude-plugin/commands/cmd.implement.md (AC1)
- [ ] T019 Manual test: Run /implement on this feature (005-phase-task-files) to verify phase files and manifest are generated correctly (Integration test)
- [ ] T020 Manual verification: Check that tasks/ directory exists with phase_1.md through phase_6.md and manifest.json (Integration test)

---

## Spec Requirement Mapping

- **AC1** (Phase files created in tasks/ directory): T001, T002, T006, T017, T018
- **AC2** (Phase files contain all tasks for that phase): T003, T004, T005, T006, T007, T008, T009
- **AC3** (manifest.json with minimal metadata): T004, T010, T011, T012, T013
- **AC4** (Coding agents can read files sequentially): Validated by file structure in T019-T020
- **AC5** (Status updates to JSON manifest): Out of scope - future work
- **AC6** (Programmatic task traversal): Validated by manifest structure in T010-T013
- **EC1** (Single phase handling): T014
- **EC2** (Empty phase handling): T015
- **EC3** (Special character escaping): T011
- **Risk1** (LLM parsing failures): T016

---

## Critical Dependencies

1. **Parsing before generation**: T003-T005 must be complete before T006-T009 (phase files) and T010-T013 (manifest) can reference extracted data
2. **Both outputs before integration**: T009 and T013 must be complete before T017 (workflow trigger) is added
3. **Implementation before testing**: T001-T018 must be complete before T019-T020 (manual verification)

---

## Notes

- This is purely prompt engineering - all changes are additions to .claude-plugin/commands/cmd.implement.md
- No new executable code files are created
- Testing is manual: run /implement on this feature branch and verify the output
- The self-referential test (T019-T020) will validate the implementation by running it on this very feature
- Edge cases T014-T016 can be implemented in parallel as they're independent conditional blocks
- Future work: Add programmatic status update mechanism for coding agents (AC5)
