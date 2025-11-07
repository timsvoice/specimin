# Implementation Tasks: Evaluation Framework

**Implementation Overview**

This implementation builds a fully automated evaluation framework for testing Specimin's spec→plan→implement pipeline quality. The system centers around a new `/eval` command that orchestrates the entire workflow within a Claude Code session, using the Task tool to programmatically invoke Specimin commands, execute tests, score artifacts, and generate reports. The implementation is decomposed into 6 phases: foundational test case creation, core evaluation orchestration, test execution infrastructure, LLM rubric evaluation, results reporting with baseline tracking, and final completion with documentation.

---

**Phase 1: Test Case Foundation**

### Task 1.1: Create directory structure for evaluation framework
**Context**: Establishes the organizational structure for all evaluation components.
**Acceptance Criteria**:
- Directory `.specimin/eval/` exists with subdirectories: `rubrics/`, `runs/`, `test_cases/`
- Directory structure is git-tracked (contains .gitkeep files where needed)
- Structure matches plan specification
**Dependencies**: None

### Task 1.2: Define test case JSON schema and create manifest file
**Context**: Establishes the data structure for storing all test cases in a single manifest.
**Acceptance Criteria**:
- File `.specimin/eval/test_cases.json` exists with valid JSON schema
- Schema includes fields: `id`, `name`, `feature_description`, `expected_functions`, `test_code`
- File contains empty array or initial structure ready for test cases
**Dependencies**: Task 1.1

### Task 1.3: Write 5 initial Python test cases
**Context**: Creates foundational test cases covering diverse simple feature types.
**Acceptance Criteria**:
- 5 test cases added to `test_cases.json` covering: LRU cache, rate limiter, string validator, stack data structure, simple parser
- Each test case has complete feature description (suitable for /spec command input)
- Each test case has pytest test code that validates functional correctness with flexible assertions
**Dependencies**: Task 1.2

---

**Phase 2: Evaluation Command Foundation**

### Task 2.1: Create /eval command in development commands directory
**Context**: Establishes the evaluation command as a development tool (not part of the distributable plugin).
**Acceptance Criteria**:
- Directory `.claude/commands/` exists (create if missing)
- File `.claude/commands/eval.md` exists with command metadata
- Command description explains it runs automated pipeline evaluation for Specimin development
**Dependencies**: Phase 1 complete

### Task 2.2: Create evaluation orchestrator prompt template
**Context**: Defines the core prompt that drives the evaluation workflow automation.
**Acceptance Criteria**:
- Prompt reads test_cases.json and iterates through each test case
- Prompt includes logic for invoking Task tool to run /spec, /plan, /implement for each case
- Prompt includes instructions for capturing and storing artifacts in run directory
**Dependencies**: Task 2.1

### Task 2.3: Add workspace management helper function
**Context**: Creates Python utility for managing timestamped run directories.
**Acceptance Criteria**:
- File `.specimin/eval/workspace.py` with function to create run directory with ISO8601 timestamp
- Function returns run directory path for artifact storage
- Function handles existing directories gracefully
**Dependencies**: Task 2.2

---

**Phase 3: Test Execution Infrastructure**

### Task 3.1: Create Python test executor module
**Context**: Provides programmatic interface for running pytest on generated code.
**Acceptance Criteria**:
- File `.specimin/eval/test_runner.py` exists with `run_test()` function
- Function accepts generated code string, test code string, and returns pass/fail result
- Function distinguishes syntax errors from test assertion failures
**Dependencies**: Phase 2 complete

### Task 3.2: Add test result capture and formatting
**Context**: Structures test execution results for reporting.
**Acceptance Criteria**:
- Test runner captures stdout, stderr, and exit code
- Test runner returns structured dict with: test_id, passed (bool), error_type, error_message
- Error types differentiate: syntax_error, assertion_failure, execution_error
**Dependencies**: Task 3.1

### Task 3.3: Integrate test execution into eval orchestrator
**Context**: Connects test running to the main evaluation workflow.
**Acceptance Criteria**:
- Orchestrator invokes test_runner.py for each test case after code generation
- Test results are stored in run directory as `test_results.json`
- Orchestrator continues evaluation even if individual tests fail
**Dependencies**: Task 3.2

---

**Phase 4: LLM Rubric Evaluation**

### Task 4.1: Create rubric prompt template for spec evaluation
**Context**: Defines the structured prompt for scoring specification quality on 3 dimensions.
**Acceptance Criteria**:
- File `.specimin/eval/rubrics/spec_rubric.md` exists
- Template includes scoring instructions for: Completeness (1-5), Clarity (1-5), Testability (1-5)
- Template provides clear definition for each score level with examples
**Dependencies**: Phase 3 complete

### Task 4.2: Create rubric prompt templates for plan and implementation evaluation
**Context**: Defines prompts for scoring plan and implementation quality.
**Acceptance Criteria**:
- File `.specimin/eval/rubrics/plan_rubric.md` includes: Feasibility, Detail Level, Phase Organization
- File `.specimin/eval/rubrics/implementation_rubric.md` includes: Actionability, Granularity, Dependencies
- Both templates follow same structure as spec rubric
**Dependencies**: Task 4.1

### Task 4.3: Create artifact scoring orchestrator
**Context**: Automates LLM rubric scoring using Task tool within evaluation session.
**Acceptance Criteria**:
- Orchestrator reads rubric templates and artifact files
- Orchestrator invokes Task tool with general-purpose agent to score each artifact
- Scores are parsed from agent responses and validated (1-5 range per dimension)
**Dependencies**: Task 4.2

### Task 4.4: Integrate rubric scoring into eval orchestrator
**Context**: Adds artifact quality evaluation to the main pipeline.
**Acceptance Criteria**:
- After each test case completes, artifacts are scored via Task tool
- Rubric scores stored in run directory as `rubric_scores.json`
- Scoring failures (invalid responses) are logged but don't halt evaluation
**Dependencies**: Task 4.3

---

**Phase 5: Results & Reporting**

### Task 5.1: Create report generation module
**Context**: Compiles all test results and artifact scores into structured output.
**Acceptance Criteria**:
- File `.specimin/eval/reporter.py` with `generate_report()` function
- Function aggregates test results and rubric scores from run directory
- Function calculates overall pass rate and per-dimension average scores
**Dependencies**: Phase 4 complete

### Task 5.2: Add formatted report output
**Context**: Generates human-readable report in addition to JSON.
**Acceptance Criteria**:
- Reporter creates `report.json` with structured data
- Reporter creates `report.md` with formatted summary (pass rate, failed tests, score breakdown)
- Both files saved to run directory
**Dependencies**: Task 5.1

### Task 5.3: Create baseline storage with append logic
**Context**: Maintains historical record of all evaluation runs for trend analysis.
**Acceptance Criteria**:
- File `.specimin/eval/baselines.json` is created if missing (empty array)
- Each run's summary is appended to baselines with timestamp, pass rate, average scores
- JSON remains valid after append operations
**Dependencies**: Task 5.2

### Task 5.4: Add regression detection function
**Context**: Compares current run against previous baselines to identify degradation.
**Acceptance Criteria**:
- Function compares current pass rate to most recent baseline
- Function flags regression if pass rate drops >5% from previous run
- Regression warning included in report.md if detected
**Dependencies**: Task 5.3

### Task 5.5: Display summary in eval command output
**Context**: Provides immediate feedback when evaluation completes.
**Acceptance Criteria**:
- Orchestrator displays summary: total tests, passed/failed count, pass rate, regression status
- Summary includes link to full report in run directory
- Clear indication of success (≥80% pass rate) or failure
**Dependencies**: Task 5.4

---

**Phase 6: Completion**

### Task 6.1: Add 5-10 additional test cases to reach target count
**Context**: Expands test coverage to meet the 10-15 test case requirement.
**Acceptance Criteria**:
- Total test cases in `test_cases.json` reaches 10-15
- New cases cover diverse scenarios: hash table, binary search, JSON parser, URL validator, fibonacci cache, etc.
- All new cases have complete feature descriptions and pytest tests
**Dependencies**: Phase 5 complete

### Task 6.2: Write comprehensive README documentation
**Context**: Provides usage guide for running evaluations and interpreting results.
**Acceptance Criteria**:
- File `.specimin/eval/README.md` exists with sections: Overview, Prerequisites, Usage (`/eval` command), Test Case Format, Rubric Definitions, Interpreting Results
- Documentation includes examples of report output
- Instructions for adding new test cases are clear
**Dependencies**: Task 6.1

### Task 6.3: Add environment check to eval orchestrator
**Context**: Verifies prerequisites before starting evaluation to fail fast.
**Acceptance Criteria**:
- Orchestrator checks for python3 and pytest availability at startup
- Orchestrator displays installation instructions if prerequisites missing
- Check fails gracefully with clear error messages and exits early
**Dependencies**: Task 6.2

### Task 6.4: Run full evaluation to establish initial baseline
**Context**: Validates the entire framework works end-to-end and creates first baseline.
**Acceptance Criteria**:
- Successfully run `/eval` command on all test cases
- Generate first baseline entry in `baselines.json`
- Verify report generation and all components work together
**Dependencies**: Task 6.3

---

**Cross-Phase Dependencies**
- Phase 2 requires Phase 1 (test cases must exist before command can run)
- Phase 3 requires Phase 2 (test execution needs orchestration framework)
- Phase 4 requires Phase 3 (rubric scoring happens after test execution)
- Phase 5 requires Phase 4 (reporting aggregates test and rubric results)
- Phase 6 requires Phase 5 (expansion builds on working infrastructure)

---

**Integration Notes**

This implementation creates a new `/eval` development command (in `.claude/commands/`) that fully automates the evaluation workflow. The command uses the Task tool to programmatically invoke `/spec`, `/plan`, and `/implement` commands for each test case, capturing their outputs as artifacts. Test execution happens via Python subprocess calls to pytest. Rubric scoring uses the Task tool with general-purpose agents to evaluate artifacts against scoring templates. The entire pipeline runs within a single Claude Code session with no manual intervention required. Results are stored in timestamped run directories with both JSON and markdown reports, and historical baselines enable regression tracking across evaluation runs. The `/eval` command is a development tool for testing Specimin quality and is not part of the distributable plugin.
