## **Objective**

Create an interactive Claude Code command (`/cmd.implement`) that generates atomic implementation tasks from high-level plans, providing coding agents with clear, actionable work items.

## **Context**

After creating a specification (`/cmd.spec`) and high-level plan (`/cmd.feature.plan`), developers need implementation broken into atomic tasks. These tasks must be function-level specific but avoid prescribing code, giving coding agents clarity on *what* to build while preserving flexibility on *how*.

## **Assumptions**

- Plan exists at `.specimin/plans/{branch}/plan.md` before implementation document generation
- Coding preferences come from a separate higher-level document (not defined here)
- Atomic means function-level granularity (e.g., "Create validation function for email input")
- Tasks grouped by phase with dependencies, context, and acceptance criteria
- Coding agent has access to plan.md and spec.md for full context

## **Constraints**

- Must follow interactive flow: Clarify plan ambiguities → Generate draft → Refine → Finalize
- Must read plan.md from `.specimin/plans/{branch}/` directory
- Tasks must be function-level atomic but never include code/pseudocode
- Questions resolve plan ambiguities only (not coding style/preferences)
- Output format: Phased task groups with context, rationale, acceptance criteria per task
- Final document saved to `.specimin/plans/{branch}/implementation.md`
- Must be economical in length (preserve token budget for coding agent)
- Formatted as Claude Code slash command in `.claude/commands/cmd.implement.md`

## **Acceptance Criteria**

- Command reads plan from `.specimin/plans/{branch}/plan.md` automatically
- Stage 1 asks 2-5 clarifying questions about plan ambiguities/unclear aspects
- Tasks are function-level atomic (not component-level or code-level)
- Each task specifies WHAT to accomplish, not HOW
- Tasks grouped into phases matching plan structure
- Each task includes: description, rationale, acceptance criteria, dependencies
- Stage 3 allows iterative refinement until approval
- Saved only after approval to `.specimin/plans/{branch}/implementation.md`
- Document is concise (minimize token overhead for coding agents)

## **User Scenarios**

1. **Standard flow**: User runs `/cmd.implement` → Reads plan.md → Identifies 3 ambiguities → Asks questions → User clarifies → Generates 15 atomic tasks in 4 phases → User approves → Saved

2. **Complex integration**: Plan says "Add authentication middleware" → Asks about existing middleware patterns, error flow → User clarifies → Breaks into tasks: "Create auth validation function", "Create token verification function", "Create error response handler", "Wire middleware into router"

3. **Unclear dependencies**: Plan lists tasks but dependency order unclear → Asks "Should data migration happen before or after schema updates?" → User decides → Tasks ordered with explicit dependency markers

## **Edge Cases**

- Plan.md doesn't exist → Prompt user for path
- Plan too vague to create atomic tasks → Ask for plan clarification before proceeding
- User wants more/less granular tasks → Adjust atomicity and regenerate
- Tasks span multiple phases → Mark cross-phase dependencies explicitly
- Plan changes during implementation → Detect mismatch, ask if regeneration needed

## **Dependencies**

- Plan.md must exist (created by `/cmd.feature.plan`)
- Spec.md exists at `.specimin/plans/{branch}/spec.md` (for reference context)
- Git branch corresponds to feature directory

## **Out of Scope**

- Generating code or pseudocode
- Defining coding style/conventions (comes from separate document)
- Auto-executing tasks (coding agent responsibility)
- Validating or editing plan.md
- Multi-branch implementation (only current branch)
- Test generation (tasks specify acceptance criteria only)
