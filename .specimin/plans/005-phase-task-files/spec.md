**Objective**

Implement phase-based task file generation during the implementation phase to provide coding agents with focused, manageable work chunks and enable programmatic task traversal.

**Context**

Currently, the implementation phase presents all tasks in a single large document, making it difficult for coding agents to maintain focus and for the system to track progress programmatically. By chunking tasks into phase files with a JSON manifest, we enable:
- Better agent focus on discrete work phases
- Programmatic task navigation and status tracking
- Clear progress visibility across the implementation lifecycle

**Assumptions**

- The `/specimin:cmd.implement` command generates an `implementation.md` file with phase-structured tasks
- Phases are clearly delineated in the implementation.md output
- LLM agents have sufficient context to parse implementation.md and create structured phase files
- JSON manifest serves as the authoritative source for task status
- Each phase contains a manageable number of tasks (typically 5-15)

**Constraints**

- Must integrate with existing Specimin directory structure (`.specimin/plans/{branch}/`)
- LLM agent must handle all file creation and initial JSON generation
- JSON manifest must be machine-parsable for external tooling
- Phase files must remain human-readable markdown
- Must work within the existing `/specimin:cmd.implement` workflow

**Acceptance Criteria**

- When `/specimin:cmd.implement` completes, phase files are created in `.specimin/plans/{branch}/tasks/`
- Each phase file contains all tasks for that phase in markdown format
- A `manifest.json` file exists in the tasks directory with minimal task metadata
- JSON manifest includes: task ID, description, phase number, and status field
- Coding agents can read phase files sequentially to execute tasks
- Task status updates are written to JSON manifest, not markdown files
- System can programmatically determine which phase to work on next via JSON

**User Scenarios**

1. **Initial task generation**: User runs `/specimin:cmd.implement` → Agent reads implementation.md → Creates `phase_1.md`, `phase_2.md`, etc. → Generates `manifest.json` with all tasks in "pending" status

2. **Coding agent execution**: Coding agent queries manifest.json for next pending task → Reads corresponding phase file for context → Executes task → Updates task status in manifest.json to "completed"

3. **Progress tracking**: User/system reads manifest.json → Calculates completion percentage → Identifies current phase → Determines remaining work

4. **Phase transition**: Agent completes all tasks in phase_1.md → Manifest shows Phase 1 100% complete → Agent automatically begins phase_2.md

**Edge Cases**

- Implementation.md has only one phase (create single phase file, not phase_1.md)
- Phase contains no tasks (skip file creation, document in manifest)
- Task descriptions contain special characters that break JSON (proper escaping required)
- Multiple agents attempt to update manifest.json simultaneously (file locking or atomic writes)
- Agent crashes mid-phase (manifest preserves completed task status for resume)
- Implementation.md is regenerated (determine whether to overwrite or merge with existing task status)

**Dependencies**

- Existing `/specimin:cmd.implement` command that generates implementation.md
- `.specimin/plans/{branch}/` directory structure already created
- LLM agent has Write tool access for file creation
- Implementation.md follows consistent phase structure/formatting

**Out of Scope**

- Web UI for task visualization
- Git integration for task status commits
- Multi-agent coordination or task locking mechanisms
- Task time estimation or velocity tracking
- Rollback or undo functionality for task status
- Task dependency validation beyond phase ordering
- Integration with external project management tools
