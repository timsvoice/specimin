# Implementation Tasks: Refactor Specimin Plugin to Use Agent Skills

**Overview**: Migrate four core workflow commands (spec, plan, task, wrap) from slash commands to Agent Skills bundled in `.claude-plugin/skills/`, with supporting scripts moved into each skill's scripts/ subdirectory.

**Total Tasks**: 21 | **Phases**: 3 | **Estimated Completion**: 3-4 hours

---

## Phase 1: Foundation Setup
**Dependencies**: None
**Parallel Opportunities**: 4 (T002-T005 can run in parallel)

- [ ] T001 Create skills directory structure at .claude-plugin/skills/ (R01)
- [ ] T002 [P] Audit tool requirements from cmd.spec.md and document needed tools (R02)
- [ ] T003 [P] Audit tool requirements from cmd.plan.md and document needed tools (R02)
- [ ] T004 [P] Audit tool requirements from cmd.task.md and document needed tools (R02)
- [ ] T005 [P] Audit tool requirements from cmd.wrap.md and document needed tools (R02)
- [ ] T006 Document SKILL.md structure with YAML frontmatter requirements in temporary reference file (R01, R03)

---

## Phase 2: Skill Migration (Core Workflows)
**Dependencies**: Phase 1 complete
**Parallel Opportunities**: 8 (directory creation and skill creation can be parallelized)

- [ ] T007 [P] Create .claude-plugin/skills/specimin-spec/ directory (R01)
- [ ] T008 [P] Create .claude-plugin/skills/specimin-spec/scripts/ directory and copy save-spec.sh and setup.feature.sh from .specimin/ (R06)
- [ ] T009 [P] Create .claude-plugin/skills/specimin-spec/SKILL.md with content from cmd.spec.md, add frontmatter with name, description, allowed-tools, and update script references to scripts/ (R01, R02, R03, R06)
- [ ] T010 [P] Create .claude-plugin/skills/specimin-plan/ directory (R01)
- [ ] T011 [P] Create .claude-plugin/skills/specimin-plan/scripts/ directory and copy save-plan.sh from .specimin/ (R06)
- [ ] T012 [P] Create .claude-plugin/skills/specimin-plan/SKILL.md with content from cmd.plan.md, add frontmatter with name, description, allowed-tools, and update script references to scripts/ (R01, R02, R03, R06)
- [ ] T013 [P] Create .claude-plugin/skills/specimin-task/ directory (R01)
- [ ] T014 [P] Create .claude-plugin/skills/specimin-task/SKILL.md with content from cmd.task.md, add frontmatter with name, description, and allowed-tools (R01, R02, R03)
- [ ] T015 [P] Create .claude-plugin/skills/specimin-wrap/ directory (R01)
- [ ] T016 [P] Create .claude-plugin/skills/specimin-wrap/SKILL.md with content from cmd.wrap.md, add frontmatter with name, description, and allowed-tools (R01, R02, R03)

---

## Phase 3: Plugin Configuration
**Dependencies**: Phase 2 complete
**Parallel Opportunities**: 0 (plugin.json must be updated before deprecating commands)

- [ ] T017 Update .claude-plugin/plugin.json to add "skills" array with paths to four skill directories (R01)
- [ ] T018 Rename .claude-plugin/commands/cmd.spec.md to cmd.spec.md.deprecated (R04)
- [ ] T019 Rename .claude-plugin/commands/cmd.plan.md to cmd.plan.md.deprecated (R04)
- [ ] T020 Rename .claude-plugin/commands/cmd.task.md to cmd.task.md.deprecated (R04)
- [ ] T021 Rename .claude-plugin/commands/cmd.wrap.md to cmd.wrap.md.deprecated (R04)

---

## Spec Requirement Mapping
- R01 (Four new SKILL.md files created): Tasks T001, T006, T007, T009, T010, T012, T013, T014, T015, T016, T017
- R02 (Appropriate allowed-tools list): Tasks T002, T003, T004, T005, T009, T012, T014, T016
- R03 (Description states explicit user intent): Tasks T006, T009, T012, T014, T016
- R04 (Slash command files deprecated): Tasks T018, T019, T020, T021
- R05 (Init and refactor remain): No tasks (unchanged, not deprecated)
- R06 (Skills reference shell scripts correctly): Tasks T008, T009, T011, T012

---

## Critical Dependencies
1. Phase 1 must complete before Phase 2 (need tool audit and directory structure)
2. Phase 2 must complete before Phase 3 (skills must exist before configuring plugin.json)
3. T017 (update plugin.json) must complete before T018-T021 (deprecation) to ensure skills are registered before commands are deprecated
4. Scripts must be copied before SKILL.md files are created (T008 before T009, T011 before T012)

---

## Notes
- **Tool Audit**: Each command file needs analysis to identify which Claude Code tools it uses (Read, Write, Bash, Grep, Glob, AskUserQuestion, Edit, etc.)
- **SKILL.md Format**: Must include YAML frontmatter with `name`, `description`, and `allowed-tools` fields, followed by markdown content
- **Description Pattern**: Should state "Use only when user explicitly requests..." to follow explicit user intent requirement
- **Script Path Pattern**: Use relative paths like `scripts/save-spec.sh` within each skill directory, NOT `${CLAUDE_PLUGIN_ROOT}`
- **Script Dependencies**: save-spec.sh calls setup.feature.sh, so both must be in specimin-spec/scripts/
- **Rollback Safety**: Deprecated files with .deprecated suffix allow reverting if skills don't work as expected
- **Original Scripts**: Keep originals in .specimin/ for reference and backward compatibility
- **Verification**: Skills will be tested organically through actual usage rather than formal test tasks
