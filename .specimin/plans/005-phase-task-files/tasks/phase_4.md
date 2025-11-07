# Phase 4: Manifest Generation

**Dependencies**: Phase 2 complete
**Parallel Opportunities**: 4 (entire phase can run parallel with Phase 3)

- [ ] T010 [P] Add prompt instruction to construct JSON array of task objects with schema: {id, description, phase, status} in .claude-plugin/commands/cmd.implement.md (AC3)
- [ ] T011 [P] Add prompt instruction with JSON escaping examples (quotes, backslashes, newlines) in .claude-plugin/commands/cmd.implement.md (AC3, EC3)
- [ ] T012 [P] Add prompt instruction to initialize all task status fields to "pending" in .claude-plugin/commands/cmd.implement.md (AC3)
- [ ] T013 [P] Add prompt instruction to write manifest.json using Write tool to tasks directory in .claude-plugin/commands/cmd.implement.md (AC3)
