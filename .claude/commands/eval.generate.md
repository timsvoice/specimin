# Generate Artifacts for Evaluation Test Case

Generate spec, plan, and implementation artifacts for a single evaluation test case.

## Usage

```
/eval-generate <test_case_id>
```

Example: `/eval-generate tc001`

## Role

You are an **artifact generator** for Specimin evaluation. Your job is to generate three artifacts (spec, plan, implementation) for a test case without user interaction.

## Workflow

### Step 1: Load Test Case

1. Read test cases manifest:
   ```bash
   cat .specimin/eval/test_cases.json
   ```

2. Find the test case matching `<test_case_id>` from the arguments

3. Extract the `feature_description` field

### Step 2: Create Run Directory

1. Create version-based run directory:
   ```bash
   python3 .specimin/eval/workspace.py
   ```
   This returns a path like `.specimin/eval/runs/v1.0.0` (based on version in `.claude-plugin/plugin.json`)

2. Create test case subdirectory:
   ```bash
   mkdir -p {run_dir}/{test_case_id}
   ```

### Step 3: Generate Spec (Non-Interactive)

Instead of using `/spec` command (which asks questions), generate the spec directly:

1. Analyze the feature description
2. Make reasonable assumptions for a general-purpose implementation:
   - Use case: General-purpose utility
   - Types: Type-agnostic (flexible)
   - Simplicity: Minimal API surface
   - Thread safety: Single-threaded
   - Validation: Strict (fail fast on invalid inputs)

3. Write a complete specification following this format:

```markdown
**Objective**: [Clear statement of what needs to be built]

**Context**: [Why this is needed, use cases]

**Assumptions**: [List your reasonable assumptions]

**Constraints**: [Technical and business limitations]

**Acceptance Criteria**: [Testable, verifiable conditions]

**User Scenarios**: [Step-by-step usage flows]

**Edge Cases**: [Boundary conditions to handle]

**Dependencies**: [External requirements, if any]

**Out of Scope**: [What's explicitly excluded]
```

4. Save to: `{run_dir}/{test_case_id}/spec.md`

### Step 4: Generate Plan (Non-Interactive)

1. Read the spec you just created
2. Generate an implementation plan following the Tree-of-Thought approach
3. Include:
   - Data structures needed
   - Algorithm approach
   - Key implementation considerations
   - Testing strategy

4. Save to: `{run_dir}/{test_case_id}/plan.md`

### Step 5: Generate Implementation Tasks

1. Read both spec and plan
2. Break down into atomic, sequential implementation tasks
3. Each task should be:
   - Specific and actionable
   - Independently implementable
   - Testable

4. Save to: `{run_dir}/{test_case_id}/implementation.md`

### Step 6: Output Summary

Display to user:
```
✓ Generated artifacts for {test_case_id}

Location: {run_dir}/{test_case_id}/
Files:
  - spec.md
  - plan.md
  - implementation.md

Next step: /eval-judge {test_case_id} {run_dir}
```

## Important Notes

- **Non-interactive**: Make reasonable assumptions, don't ask questions
- **Consistent quality**: Apply same judgment you'd use for real features
- **Complete artifacts**: Each file should be production-ready
- **No shortcuts**: Generate full, detailed content as if for real development

## Error Handling

- If test case ID not found: Display error and list available IDs
- If workspace creation fails: Display error message
- If file write fails: Report which artifact failed
