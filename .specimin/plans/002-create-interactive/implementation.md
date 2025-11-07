# Implementation Tasks: Interactive Implementation Task Generator

**Implementation Overview**

This implementation creates the `/cmd.implement` slash command that converts high-level plans into atomic, function-level implementation tasks. The command follows a four-stage interactive workflow: analyzing the plan for ambiguities, asking clarifying questions, generating a draft task breakdown, and iteratively refining until user approval before saving to implementation.md.

---

**Phase 1: Command File Creation**

### Task 1.1: Create cmd.implement.md command file with frontmatter
**Context**: Establishes the slash command in Claude Code's command system
**Acceptance Criteria**:
- File created at `.claude/commands/cmd.implement.md`
- Frontmatter includes description field matching spec objective
- Description appears when user types `/cmd.implement`
**Dependencies**: None

### Task 1.2: Add Stage 1 workflow instructions for reading plan and spec files
**Context**: Command needs to automatically locate and read plan.md and spec.md based on current git branch
**Acceptance Criteria**:
- Instructions include git branch detection command
- Instructions specify reading from `.specimin/plans/{branch}/plan.md`
- Instructions specify reading from `.specimin/plans/{branch}/spec.md`
- Flow proceeds to analysis after successful reads
**Dependencies**: Task 1.1

### Task 1.3: Add semantic analysis instructions for plan ambiguities
**Context**: Claude must dynamically determine what's unclear in the plan without fixed detection logic
**Acceptance Criteria**:
- Instructions guide analysis of dependencies, integration points, error handling
- Focus on blocking ambiguities that prevent technical choices
- No rigid ambiguity detection rules (Claude uses judgment)
- Analysis identifies 0-5 questions to ask
**Dependencies**: Task 1.2

### Task 1.4: Add question generation instructions with format template
**Context**: When ambiguities found, command must ask focused questions with concrete options
**Acceptance Criteria**:
- Question format matches specification (What's unclear, Options A/B/Custom)
- Maximum 2-5 questions enforced
- Questions focus on plan-level ambiguities only (not coding style)
- Instructions include wait-for-response behavior
**Dependencies**: Task 1.3

---

**Phase 2: Task Generation Logic**

### Task 2.1: Add instructions for atomic task decomposition using input/output boundary heuristic
**Context**: Core logic that breaks plan's task sequence into function-level units
**Acceptance Criteria**:
- Instructions define function-level atomicity with examples
- Guidance on identifying input/output boundaries as task boundaries
- Examples of too-broad vs too-granular tasks included
- Instructions forbid code, pseudocode, or implementation details
**Dependencies**: Phase 1 complete

### Task 2.2: Add task formatting instructions for minimal context preservation
**Context**: Each task needs description, context, acceptance criteria, and dependencies in token-efficient format
**Acceptance Criteria**:
- Format template matches: description, context, acceptance criteria, dependencies
- Instructions emphasize brevity (minimal tokens)
- Behavioral checklist format for acceptance criteria specified
- Phase-based dependency notation explained
**Dependencies**: Task 2.1

### Task 2.3: Add phase grouping instructions matching plan structure
**Context**: Tasks must be organized into phases that mirror the plan's phase structure
**Acceptance Criteria**:
- Instructions specify extracting phase names from plan
- Tasks numbered within phases (1.1, 1.2, 2.1, etc.)
- Phase dependencies noted (Phase 2 depends on Phase 1)
- Cross-phase dependencies handled explicitly when needed
**Dependencies**: Task 2.2

### Task 2.4: Add output format template for implementation.md structure
**Context**: Generated document needs consistent structure for coding agents to parse
**Acceptance Criteria**:
- Template includes: Implementation Overview, Phase sections, Task subsections, Cross-Phase Dependencies, Integration Notes
- Format matches specification example output
- Instructions ensure WHAT-focused task descriptions (not HOW)
**Dependencies**: Task 2.3

---

**Phase 3: Iteration and Refinement**

### Task 3.1: Add Stage 3 review prompt instructions
**Context**: After generating draft, command must ask user for feedback and support refinement
**Acceptance Criteria**:
- Prompt asks: "Do these tasks match what you need? Should I adjust granularity or add/remove anything?"
- Instructions explain how to wait for user response
- Multiple iteration rounds supported
**Dependencies**: Phase 2 complete

### Task 3.2: Add regeneration instructions with context retention
**Context**: When user requests changes, command must remember previous context and adjust task breakdown
**Acceptance Criteria**:
- Instructions specify retaining plan analysis and user's earlier clarifications
- Guidance on adjusting granularity (more/less atomic)
- Guidance on adding/removing/reordering tasks
- Instructions loop back to task generation with modifications
**Dependencies**: Task 3.1

---

**Phase 4: Finalization and Error Handling**

### Task 4.1: Add Stage 4 save instructions with path resolution
**Context**: After approval, document must be saved to correct location based on branch
**Acceptance Criteria**:
- Instructions include git branch command for path resolution
- Save path is `.specimin/plans/{branch}/implementation.md`
- Confirmation message includes full path
- Only saves after explicit user approval
**Dependencies**: Phase 3 complete

### Task 4.2: Add error handling instructions for missing plan.md
**Context**: Command must detect and handle case when plan.md doesn't exist
**Acceptance Criteria**:
- Instructions check for plan.md existence before reading
- Error message is helpful and actionable
- Exits workflow with instructions (does not continue)
- No custom path prompting (exit-only behavior)
**Dependencies**: Task 1.2

### Task 4.3: Add detection instructions for overly vague plans
**Context**: When plan lacks sufficient detail for atomic tasks, command should warn user
**Acceptance Criteria**:
- Instructions guide detection of insufficient plan detail
- Warning message asks user to add detail to plan.md first
- Suggests what kinds of details are missing
- Workflow pauses until plan is improved
**Dependencies**: Task 1.3

### Task 4.4: Add granularity adjustment guidance instructions
**Context**: User may request more or less granular task breakdown during iteration
**Acceptance Criteria**:
- Instructions explain how to respond to "make tasks smaller" requests
- Instructions explain how to respond to "make tasks larger" requests
- Guidance on maintaining function-level boundaries
- Examples of granularity adjustments included
**Dependencies**: Task 3.2

---

**Cross-Phase Dependencies**
- Task 4.2 depends on Task 1.2 (error handling for file reading setup)
- Task 4.3 depends on Task 1.3 (error handling for ambiguity analysis)
- Task 4.4 depends on Task 3.2 (granularity guidance extends regeneration capability)

---

**Integration Notes**

The command integrates with the existing Claude Code slash command system by placing the prompt file in `.claude/commands/` with proper frontmatter. It relies on git for branch detection and the established `.specimin/plans/{branch}/` directory structure created by earlier commands in the workflow (/cmd.spec, /cmd.feature.plan). The command outputs to implementation.md, which serves as input for coding agents executing the actual implementation work.
