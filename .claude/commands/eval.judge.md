# Judge Evaluation Artifacts

Score generated artifacts (spec, plan, implementation) using LLM-based rubrics.

## Usage

```
/eval-judge <test_case_id> <run_dir>
```

Example: `/eval-judge tc001 .specimin/eval/runs/v1.0.0`

## Role

You are an **impartial quality evaluator** assessing Specimin-generated artifacts against objective rubrics. Score each artifact honestly - this helps improve the system.

## Workflow

### Step 1: Load Test Case and Artifacts

1. Read test case from manifest:
   ```bash
   cat .specimin/eval/test_cases.json
   ```
   Extract the test case matching `<test_case_id>`

2. Read generated artifacts:
   ```bash
   cat {run_dir}/{test_case_id}/spec.md
   cat {run_dir}/{test_case_id}/plan.md
   cat {run_dir}/{test_case_id}/implementation.md
   ```

### Step 2: Score Specification

Evaluate the spec.md against this rubric (score 0-4 for each criterion):

**Clarity (0-4)**
- 4: Crystal clear objectives, context, and acceptance criteria with no ambiguity
- 3: Clear with minor ambiguities that don't affect implementation
- 2: Somewhat clear but missing key details
- 1: Vague or confusing in multiple areas
- 0: Incomprehensible or missing critical sections

**Completeness (0-4)**
- 4: All required sections present with comprehensive detail
- 3: All sections present with minor gaps
- 2: Missing 1-2 important sections or major gaps
- 1: Missing multiple key sections
- 0: Severely incomplete or empty

**Testability (0-4)**
- 4: All acceptance criteria are concrete, measurable, and testable
- 3: Most criteria testable with minor ambiguities
- 2: Some criteria testable, others vague
- 1: Few testable criteria
- 0: No testable acceptance criteria

**Scope Appropriateness (0-4)**
- 4: Scope perfectly matches feature description, clear boundaries
- 3: Scope mostly appropriate with minor deviations
- 2: Scope somewhat misaligned (too broad or too narrow)
- 1: Scope significantly misaligned
- 0: Scope completely wrong or undefined

### Step 3: Score Plan

Evaluate the plan.md against this rubric (score 0-4 for each criterion):

**Technical Soundness (0-4)**
- 4: Proposed approach is optimal and considers tradeoffs
- 3: Solid approach with minor inefficiencies
- 2: Workable approach but suboptimal
- 1: Questionable approach with significant issues
- 0: Fundamentally flawed approach

**Clarity (0-4)**
- 4: Implementation path is crystal clear and unambiguous
- 3: Clear with minor areas needing clarification
- 2: Somewhat clear but missing important details
- 1: Confusing or hard to follow
- 0: Incomprehensible

**Completeness (0-4)**
- 4: Addresses all aspects from spec with thorough detail
- 3: Covers most aspects with minor gaps
- 2: Missing some important aspects
- 1: Many critical gaps
- 0: Severely incomplete

**Feasibility (0-4)**
- 4: Highly implementable with clear, actionable steps
- 3: Implementable with minor clarifications needed
- 2: Implementable but requires significant interpretation
- 1: Difficult to implement as described
- 0: Not implementable

### Step 4: Score Implementation Tasks

Evaluate the implementation.md against this rubric (score 0-4 for each criterion):

**Atomicity (0-4)**
- 4: All tasks are perfectly atomic and independently implementable
- 3: Most tasks atomic with 1-2 that could be split
- 2: Some tasks too large or too small
- 1: Many tasks poorly scoped
- 0: Tasks are not atomic at all

**Clarity (0-4)**
- 4: Every task is crystal clear and actionable
- 3: Most tasks clear with minor ambiguities
- 2: Some tasks vague or unclear
- 1: Many tasks confusing
- 0: Tasks are incomprehensible

**Completeness (0-4)**
- 4: All implementation aspects from plan are covered
- 3: Most aspects covered with minor gaps
- 2: Some important aspects missing
- 1: Many critical aspects missing
- 0: Severely incomplete

**Sequencing (0-4)**
- 4: Perfect logical order with clear dependencies
- 3: Good ordering with minor improvements possible
- 2: Some ordering issues affecting efficiency
- 1: Poor ordering causing confusion
- 0: Random or illogical order

### Step 5: Save Scores

Create a JSON file with all scores:

```json
{
  "test_case_id": "tc001",
  "timestamp": "2025-10-29T19:54:17",
  "spec_scores": {
    "clarity": 4,
    "completeness": 3,
    "testability": 4,
    "scope_appropriateness": 4,
    "total": 15,
    "max_possible": 16,
    "percentage": 93.75,
    "notes": "Brief explanation of scoring decisions"
  },
  "plan_scores": {
    "technical_soundness": 3,
    "clarity": 4,
    "completeness": 3,
    "feasibility": 4,
    "total": 14,
    "max_possible": 16,
    "percentage": 87.5,
    "notes": "Brief explanation of scoring decisions"
  },
  "implementation_scores": {
    "atomicity": 4,
    "clarity": 4,
    "completeness": 3,
    "sequencing": 4,
    "total": 15,
    "max_possible": 16,
    "percentage": 93.75,
    "notes": "Brief explanation of scoring decisions"
  },
  "overall": {
    "total": 44,
    "max_possible": 48,
    "percentage": 91.67
  }
}
```

Save to: `{run_dir}/{test_case_id}/scores.json`

### Step 6: Display Summary

Show user:
```
✓ Scored artifacts for {test_case_id}

Spec:           {spec_percentage}% ({spec_total}/{spec_max})
  - Clarity: {score}
  - Completeness: {score}
  - Testability: {score}
  - Scope: {score}

Plan:           {plan_percentage}% ({plan_total}/{plan_max})
  - Technical Soundness: {score}
  - Clarity: {score}
  - Completeness: {score}
  - Feasibility: {score}

Implementation: {impl_percentage}% ({impl_total}/{impl_max})
  - Atomicity: {score}
  - Clarity: {score}
  - Completeness: {score}
  - Sequencing: {score}

Overall:        {overall_percentage}% ({overall_total}/{overall_max})

Scores saved to: {run_dir}/{test_case_id}/scores.json
```

## Scoring Guidelines

- **Be objective**: Score what's actually there, not what could be there
- **Be consistent**: Apply same standards across all test cases
- **Be honest**: Low scores help identify areas to improve
- **Provide notes**: Brief explanation helps understand the scores
- **No grade inflation**: Reserve 4s for truly excellent work

## Important Notes

- Scores should reflect quality relative to the rubric, not perfection
- A score of 3 is "good" - don't default to 4
- Include brief notes explaining scoring rationale
- This data helps improve Specimin over time
