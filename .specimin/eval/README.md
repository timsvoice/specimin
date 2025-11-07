# Specimin Evaluation Framework

Automated quality control system for testing Specimin's spec→plan→implement pipeline.

## Overview

This framework validates that Specimin commands produce high-quality artifacts that result in functionally correct code. It executes test cases through the full pipeline, runs functional tests on generated code, scores artifact quality using LLM rubrics, and tracks performance over time with regression detection.

**Primary Success Metric**: Functional correctness (≥80% test pass rate)
**Diagnostic Metrics**: Artifact quality scores (specs, plans, implementations)

## Prerequisites

- Python 3.8+
- pytest (`pip install pytest`)
- Claude Code (for running `/eval` command)
- Git repository

## Usage

### Running an Evaluation

Simply run the `/eval` command in Claude Code:

```
/eval
```

The evaluation will:
1. Load all test cases from `test_cases.json`
2. For each test case, invoke Specimin commands to generate artifacts
3. Execute pytest tests on generated Python code
4. Score artifacts using LLM-as-judge rubrics
5. Generate comprehensive report with pass rate and quality scores
6. Save baseline for regression tracking

### Results

Results are stored in `.specimin/eval/runs/v{version}/` (version from `.claude-plugin/plugin.json`):
- `report.json` - Structured test results and scores
- `report.md` - Human-readable summary report
- `{test_id}/` - Individual test case artifacts (spec, plan, implementation, code, test results)

Historical baselines are tracked in `.specimin/eval/baselines.json`.

## Test Case Format

Test cases are defined in `test_cases.json` with the following schema:

```json
{
  "id": "tc001",
  "name": "Feature Name",
  "feature_description": "Description to pass to /spec command",
  "expected_functions": ["ClassName", "method_name"],
  "test_code": "pytest test code as string",
  "notes": "Optional notes about the test case"
}
```

### Adding New Test Cases

1. Edit `.specimin/eval/test_cases.json`
2. Add a new test case object to the `test_cases` array
3. Follow the schema above
4. Ensure `test_code` uses flexible assertions (test behavior, not exact implementation)

**Test Code Guidelines**:
- Import implementation module as `implementation`
- Use pytest syntax
- Be flexible on implementation details (e.g., accept `None` or `-1` for missing values)
- Test behavior, not internal structure
- Keep tests focused on core functionality

### Example Test Case

```json
{
  "id": "tc011",
  "name": "Priority Queue",
  "feature_description": "Implement a min-heap priority queue...",
  "expected_functions": ["PriorityQueue", "push", "pop", "peek"],
  "test_code": "import pytest\n\ndef test_priority_queue_min_heap(implementation):\n    pq = implementation.PriorityQueue()\n    pq.push(5)\n    pq.push(2)\n    pq.push(8)\n    assert pq.pop() == 2\n    assert pq.pop() == 5\n",
  "notes": "Test min-heap property"
}
```

## Rubric Definitions

### Spec Rubric (3 dimensions, 1-5 scale)

1. **Completeness**: Does the spec include all necessary information?
   - 5: All elements present (objective, constraints, acceptance criteria, edge cases)
   - 3: Core elements present, some gaps
   - 1: Fundamentally incomplete

2. **Clarity**: Is the spec understandable and unambiguous?
   - 5: Crystal clear, no ambiguity
   - 3: Understandable with some effort
   - 1: Very unclear or contradictory

3. **Testability**: Can the spec be verified through testing?
   - 5: All criteria measurable, tests obvious
   - 3: Some criteria measurable
   - 1: No measurable criteria

### Plan Rubric (3 dimensions, 1-5 scale)

1. **Feasibility**: Is the technical approach sound?
   - 5: Well-reasoned, practical, appropriate technologies
   - 3: Some questionable choices but implementable
   - 1: Technically unsound

2. **Detail Level**: Is there sufficient detail to implement?
   - 5: Clear components, specific technologies, defined integration
   - 3: High-level components, some vagueness
   - 1: Almost no specific details

3. **Phase Organization**: Are tasks logically sequenced?
   - 5: Clear phases, logical dependencies
   - 3: Phases present but not optimal
   - 1: No logical structure

### Implementation Rubric (3 dimensions, 1-5 scale)

1. **Actionability**: Can developers immediately start working?
   - 5: Clear acceptance criteria, obvious "done" definition
   - 3: Tasks need some interpretation
   - 1: Too vague to implement

2. **Granularity**: Are tasks appropriately sized?
   - 5: Function-level boundaries, 1-4 hour tasks
   - 3: Mix of appropriate and inappropriate sizing
   - 1: All tasks too large or too small

3. **Dependencies**: Are dependencies clear and correct?
   - 5: All dependencies explicit, no circular deps
   - 3: Some dependencies identified
   - 1: Dependencies missing or wrong

## Interpreting Results

### Pass Rate

- **≥80%**: ✅ PASSING - Specimin commands are producing quality artifacts
- **<80%**: ❌ FAILING - Quality degradation detected

### Regression Detection

The framework compares each run to the previous baseline:
- **Regression**: Pass rate drops >5% from previous run
- **Improvement**: Pass rate increases
- **Stable**: Pass rate changes ≤5%

### Artifact Quality Scores

Average scores across all test cases for each dimension:
- **4.0-5.0**: Excellent quality
- **3.0-3.9**: Good quality, minor improvements possible
- **2.0-2.9**: Needs improvement
- **<2.0**: Significant quality issues

### Diagnostic Workflow

When tests fail:
1. Check `report.md` for overall summary
2. Identify failed test cases
3. Review artifact scores for that test case
4. Low spec completeness? → Spec command needs improvement
5. Low plan feasibility? → Plan command needs improvement
6. Low implementation actionability? → Implement command needs improvement

## Architecture

### Components

- **test_cases.json**: Test case manifest (10 test cases currently)
- **workspace.py**: Creates version-based run directories
- **test_runner.py**: Executes pytest on generated code
- **score_artifacts.py**: Generates LLM evaluation prompts
- **rubrics/**: Rubric templates for specs, plans, implementations
- **reporter.py**: Aggregates results into JSON and markdown reports
- **update_baseline.py**: Manages historical baselines and regression detection

### Workflow

```
/eval command
    ↓
Load test cases
    ↓
For each test case:
    - Generate spec (/spec command via Task tool)
    - Generate plan (/plan command via Task tool)
    - Generate implementation tasks (/implement via Task tool)
    - Generate code (general-purpose agent)
    - Run pytest tests
    - Score artifacts with LLM-as-judge
    ↓
Generate report
    ↓
Update baseline
    ↓
Display summary
```

## Development Notes

- This framework is a **development tool** for Specimin itself
- It is **not** part of the distributable plugin
- The `/eval` command lives in `.claude/commands/`, not `.claude-plugin/commands/`
- Test cases should remain simple and self-contained
- Rubric scoring requires active Claude Code session

## Future Enhancements

Potential improvements (not currently implemented):
- CI/CD integration for automated regression testing
- Performance benchmarking of generated code
- Multi-language support (currently Python only)
- Code quality metrics (style, security, optimization)
- Test case generation from real Specimin usage patterns
