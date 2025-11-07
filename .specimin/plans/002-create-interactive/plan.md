# Implementation Plan: Interactive Implementation Task Generator

**Technical Context**

**Existing**: Bash-based feature setup (setup.feature.sh), Git branch-based workflow, markdown command files in .claude/commands/, existing /cmd.spec and /cmd.feature.plan commands with interactive multi-stage flow

**Detected**: Claude Code slash command system, .specimin/plans/{branch}/ directory structure, spec.md and plan.md already established

**Unknowns Resolved**:
- Task granularity: Input/output boundary-based (testable units)
- Ambiguity detection: Conservative (2-3 questions max, fast workflow)
- Context preservation: Minimal (task + acceptance criteria only, ~200-400 tokens)
- Dependencies: Phase-based (clean, sequential)
- Acceptance criteria: Behavioral checklist (clear pass/fail)
- Clarification focus: Blocks to technical choices or implementation decisions

---

**Decision Exploration**

**Decision 1: Command Structure Pattern**

**Options Explored**:
- **Option A: Single monolithic prompt**
  - Advantage: Simple file structure
  - Disadvantage: Hard to maintain, no separation of concerns
  - When to use: Very simple commands

- **Option B: Multi-stage interactive flow (like /cmd.spec, /cmd.feature.plan)**
  - Advantage: Consistent with existing commands, proven pattern
  - Disadvantage: None for this use case
  - When to use: Commands requiring user input and iteration

**Selected**: Option B

**Rationale**: Matches established pattern in cmd.spec.md and cmd.feature.plan.md. Users already familiar with the flow: Analyze → Ask → Generate → Review → Save. Provides natural checkpoints for refinement.

---

**Decision 2: Plan Analysis Strategy**

**Options Explored**:
- **Option A: Regex/keyword scanning for ambiguity markers**
  - Advantage: Fast, deterministic
  - Disadvantage: Brittle, misses semantic ambiguity
  - When to use: Highly structured plans

- **Option B: LLM-based semantic analysis**
  - Advantage: Understands context, finds implicit ambiguities
  - Disadvantage: Token overhead
  - When to use: Variable plan quality

**Selected**: Option B

**Rationale**: Claude can read plan.md and identify where task order is unclear, where integration points lack detail, or where error handling isn't specified. Conservative question limit (2-3 max) keeps token cost reasonable while catching blockers.

---

**Decision 3: Task Atomicity Heuristic**

**Options Explored**:
- **Option A: Component-level (too coarse)**
  - When to use: High-level roadmaps only

- **Option B: Input/output boundary-based (testable units)**
  - Advantage: Clear definition, each task produces verifiable output
  - Disadvantage: Requires thinking about interfaces
  - When to use: When testing/verification critical (our case)

- **Option C: Line-of-code estimates (too prescriptive)**
  - When to use: Never for this spec

**Selected**: Option B

**Rationale**: "Function-level atomic" means each task produces a discrete, testable piece of functionality (e.g., "Create email validation function" not "Build auth system"). Input/output boundaries naturally define these units. Aligns with acceptance criteria format (behavioral checklist).

---

**Solution Architecture**

The command implements a four-stage interactive workflow that transforms high-level plans into function-level implementation tasks. Stage 1 reads plan.md from `.specimin/plans/{branch}/plan.md` and analyzes it for ambiguities that would block implementation—specifically unclear dependencies, missing integration details, or unspecified error handling. The command asks 2-3 conservative questions to resolve these blockers.

Stage 2 generates a draft implementation.md document by decomposing the plan's task sequence into atomic, testable units. Each task is defined by what it accomplishes (input/output boundary) and a behavioral checklist for acceptance. Tasks are grouped into phases matching the plan structure, with simple phase-based dependencies (Phase 1 → Phase 2). The document is token-minimal: task description + acceptance criteria only, as coding agents have access to plan.md and spec.md for full context.

Stage 3 presents the draft and asks "Does this capture the right task breakdown? What should I adjust?" allowing iterative refinement of granularity or task grouping. Stage 4 saves the approved document to `.specimin/plans/{branch}/implementation.md`.

The command follows the established pattern from /cmd.spec and /cmd.feature.plan: multi-stage interaction, conservative question limits, wait for approval before file creation. It operates on the current git branch to automatically resolve the feature directory path.

---

**Technology Decisions**

- Markdown format for implementation.md (consistent with spec.md, plan.md)
- Claude Code slash command system (.claude/commands/cmd.implement.md)
- Git branch name determines feature directory path (002-create-interactive → .specimin/plans/002-create-interactive/)
- Minimal context preservation strategy (~200-400 tokens total document, relying on plan.md/spec.md for detail)

---

**Component Modifications**

1. None (new command only, no modifications to existing commands)

---

**New Components**

1. **Interactive Implementation Generator** (.claude/commands/cmd.implement.md): Slash command prompt that orchestrates the four-stage workflow, reads plan.md, analyzes for ambiguities, asks clarifying questions, generates atomic task breakdown, iterates on draft, and saves final implementation.md

---

**Task Sequence**

**Phase 1: Command Prompt Creation**
1. Create .claude/commands/cmd.implement.md with frontmatter description
2. Implement Stage 1 logic: Read plan.md from `.specimin/plans/{branch}/plan.md`, analyze for blocking ambiguities (dependencies, integration, error handling), generate 2-3 focused questions
3. Implement Stage 2 logic: Transform plan task sequence into atomic function-level tasks using input/output boundary heuristic, format as minimal task + acceptance criteria, group by phases with phase-based dependencies
4. Implement Stage 3 logic: Present draft, ask for refinement feedback, support iterative adjustments
5. Implement Stage 4 logic: Save approved document to `.specimin/plans/{branch}/implementation.md`

**Dependencies**: None

---

**Phase 2: Validation & Edge Cases**
6. Add error handling for missing plan.md (prompt user for path as per spec edge case)
7. Add detection for overly vague plans (warn user that plan needs more detail before proceeding)
8. Add guidance for adjusting task granularity on user request (more/less atomic)

**Dependencies**: Phase 1

---

**Integration Points**

- **Git branch system**: Command uses `git branch --show-current` to determine feature directory path
- **File system**: Reads from `.specimin/plans/{branch}/plan.md`, writes to `.specimin/plans/{branch}/implementation.md`
- **Claude Code slash command system**: Registered in .claude/commands/ directory with description frontmatter
- **Existing spec/plan documents**: References but doesn't modify spec.md or plan.md

---

**Testing Strategy**

**Unit**: Task atomicity heuristic (verify function-level granularity), ambiguity detection (identify missing dependencies), question generation (2-3 focused questions only)

**Integration**: End-to-end flow (read plan → ask questions → generate draft → iterate → save), file I/O (correct paths based on branch name)

**E2E Flows**: Standard flow (clear plan → 2-3 questions → 15 tasks in 4 phases → approve → save), complex integration (vague plan → more clarification questions → refined task breakdown)

**Edge Cases**: Missing plan.md (prompt for path), plan too vague (request clarification), user wants different granularity (regenerate tasks), cross-phase dependencies (mark explicitly in acceptance criteria)

---

**Risk Assessment & Mitigation**

**Risk**: Tasks still too coarse-grained (not truly atomic)
**Mitigation**: Input/output boundary heuristic provides clear definition; Stage 3 iteration allows user to request more granular breakdown

**Risk**: Minimal context strategy leaves coding agents confused
**Mitigation**: Spec explicitly states coding agent has access to plan.md and spec.md; task acceptance criteria provide enough verifiability; user can request more detail in Stage 3

**Risk**: Conservative question limit (2-3) misses critical ambiguities
**Mitigation**: Focus questions on blocking issues (dependencies, integration, error handling that prevents technical choices); users familiar with workflow can request additional clarification

**Risk**: Phase-based dependencies insufficient for complex task graphs
**Mitigation**: Edge case handling allows marking cross-phase dependencies in acceptance criteria when needed; most plans follow sequential phase structure per existing cmd.feature.plan pattern
