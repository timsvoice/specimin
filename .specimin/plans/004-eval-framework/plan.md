## **Technical Context**

**Existing**: Claude Code plugin structure (`.claude-plugin/`), bash-based setup scripts, markdown slash commands (`/spec`, `/plan`, `/implement`), feature state in `.specimin/plans/{branch}/`

**Detected**: Python 3 runtime available, Git repository, JSON processing capabilities, existing command patterns with interactive workflows

**Unknowns Resolved**:
- Test case storage: Single JSON manifest for all test cases
- LLM evaluation: Leverage Claude Code's sub-agent for rubric scoring
- Pipeline execution: Interactive workflow with structured prompts (human runs commands)
- Test execution: pytest for standard, universal testing
- Baseline storage: JSON file with timestamps and full historical results
- Rubric dimensions: 3 minimal dimensions per artifact type (spec, plan, implementation)
- **Language choice: Python (most universal, best agent compatibility)**

---

## **Decision Exploration**

### Decision 1: Test Case Storage Format

**Options Explored**:
- A: Individual JSON files per test case (git-friendly, granular)
- B: Single JSON manifest with all test cases (one source of truth)
- C: Markdown with YAML frontmatter (human-readable, Specimin-style)

**Selected**: Option B

**Rationale**: For 10-15 test cases managed by a single developer, a unified manifest provides simplicity without merge conflict risks. Easier to maintain consistent schema across all tests, simpler to import into evaluation logic, and aligns with the constraint that this is a quality control tool, not a collaborative test authoring platform.

### Decision 2: LLM-as-Judge Implementation

**Options Explored**:
- A: Direct API calls with OpenAI/Anthropic SDKs (full control, costs money)
- B: Claude Code sub-agent for evaluation (free, integrated)
- C: Pattern matching heuristics (fast, deterministic, less accurate)

**Selected**: Option B

**Rationale**: Since evaluation runs within Claude Code development sessions, leveraging the existing LLM context avoids API key management and external costs. The sub-agent approach maintains consistency with Specimin's philosophy of working within Claude Code's ecosystem. Trade-off: Evaluation requires active Claude session but eliminates infrastructure dependencies.

### Decision 3: Pipeline Execution Model

**Options Explored**:
- A: Simulate command execution (fully automated, complex)
- B: Interactive with structured prompts (real commands, semi-automated)
- C: Hybrid with human coordination (flexible, multi-step)

**Selected**: Option B

**Rationale**: Matches the manual testing workflow described in constraints ("run manually during development"). Produces structured prompts that guide the human operator through running real Specimin commands for each test case, then validates outputs. This ensures evaluation tests actual command behavior, not simulated logic, while maintaining practical usability for a developer testing command improvements.

### Decision 4: Test Execution Environment

**Options Explored**:
- A: Temporary projects per test case (isolated, standard structure)
- B: Single shared project (faster, shared deps)
- C: Direct pytest execution (fastest, minimal overhead)

**Selected**: Option C

**Rationale**: Aligns perfectly with "simple, isolated features" constraint. Self-contained utilities and pure functions don't require complex project infrastructure. Direct pytest execution via `python -m pytest` provides sub-second execution per test case, meeting the <10 minute target easily for 15 tests. No dependency management overhead for straightforward pytest assertions.

### Decision 5: Baseline Storage

**Options Explored**:
- A: JSON with timestamps and full historical results (trend analysis)
- B: Single baseline.json, overwritten (simple, current state only)
- C: Git-committed results per run (version controlled)

**Selected**: Option A

**Rationale**: Supports the acceptance criterion "subsequent runs detect regressions" by maintaining history for comparison. Timestamp-indexed results enable trend analysis ("has performance degraded gradually?") and A/B testing of command variations. File growth is minimal (JSON records, not artifacts) and can accumulate dozens of runs before cleanup is needed, providing valuable diagnostic data.

### Decision 6: Rubric Dimensions

**Options Explored**:
- A: Minimal 3 dimensions per artifact (focused, essential)
- B: Comprehensive 5 dimensions (detailed diagnostics)
- C: Custom dimensions (user-specified)

**Selected**: Option A

**Rationale**: Balances diagnostic utility with evaluation speed. Three dimensions capture the most critical quality aspects without overwhelming analysis. For specs: Completeness (does it have everything?), Clarity (is it understandable?), Testability (can it be implemented and verified?). Minimal rubrics also reduce LLM evaluation time and token costs per run.

### Decision 7: Implementation Language

**Options Explored**:
- A: Elixir (functional, ExUnit, script-based execution)
- B: JavaScript/TypeScript (ubiquitous, Node/Jest, fast)
- C: Python (most universal, pytest, simple)
- D: Go (fast, built-in testing, explicit)

**Selected**: Option C (Python)

**Rationale**: Python provides the most universal test environment for validating Specimin's quality. Every coding agent has strong Python knowledge, making it the most representative language for typical Specimin usage patterns. Simple test execution via `python -m pytest` requires minimal setup, and Python's clarity makes debugging failures straightforward. The "simple, isolated features" constraint (utilities, data structures, pure functions) aligns perfectly with Python's strengths.

---

## **Solution Architecture**

The evaluation framework operates as a guided, semi-automated workflow that orchestrates three major subsystems: test case management, pipeline execution coordination, and results validation. The architecture separates test case definitions (static JSON manifest) from execution artifacts (dynamically generated) and results (timestamped historical records).

Test cases are defined in a single JSON manifest (`test_cases.json`) containing feature descriptions, expected Python module structure, and pytest test code. Each test case is self-contained: the feature description serves as input to Specimin commands, and the test code verifies the generated implementation. The manifest structure supports 10-15 cases covering varied scenarios (data structures, algorithms, simple utilities like LRU caches, rate limiters, validators).

The evaluation runner is an interactive bash script that presents test cases sequentially, prompting the human operator to run Specimin commands (`/spec`, `/plan`, `/implement`) with provided feature descriptions. The operator pastes generated artifacts back into the script, which writes them to a temporary evaluation workspace. After all artifacts are collected, the script executes validation: runs pytest against generated Python code, invokes Claude sub-agent with rubric prompts to score artifacts, and compiles results into a structured JSON report.

Results are appended to a historical baseline file (`baselines.json`) with timestamps, enabling regression detection by comparing current run's pass rate against previous runs. The report includes overall pass rate, per-test functional correctness (pass/fail), and per-artifact rubric scores (1-5 scale on 3 dimensions). This design keeps the evaluation loop tight while ensuring real command behavior is tested, not simulated logic.

---

## **Technology Decisions**

- Test case format: JSON manifest with schema (`feature_description`, `module_name`, `test_code`)
- Evaluation runner: Bash script with interactive prompts and JSON output
- **Python execution: `python -m pytest test_file.py` for standard test execution**
- LLM evaluation: Claude Code Task tool with structured rubric prompts
- Rubric dimensions: 3 per artifact type (1-5 scale scoring)
- Baseline storage: Append-only JSON with ISO8601 timestamps
- Workspace: Temporary directory (`.specimin/eval/runs/{timestamp}/`) for artifacts per run
- **Python version: 3.8+ (widely available, modern features)**

---

## **Component Modifications**

1. **None** - This feature is additive and doesn't modify existing Specimin commands or scripts

---

## **New Components**

1. **Test Case Manifest** (`.specimin/eval/test_cases.json`): JSON file defining 10-15 feature descriptions, expected Python module names, and pytest test code

2. **Evaluation Runner Script** (`.specimin/eval/run_evaluation.sh`): Bash script that prompts for command execution, collects artifacts, runs tests, scores rubrics, generates report

3. **Rubric Prompt Templates** (`.specimin/eval/rubrics/`): Markdown templates for LLM-as-judge evaluation of specs, plans, and implementations

4. **Baseline Storage** (`.specimin/eval/baselines.json`): Historical results file with timestamps, pass rates, and artifact scores

5. **Documentation** (`.specimin/eval/README.md`): Guide for running evaluations, adding test cases, interpreting results

---

## **Task Sequence**

**Phase 1: Test Case Foundation**
1. Create `.specimin/eval/` directory structure with subdirectories for test cases, rubrics, runs
2. Define JSON schema for test case manifest (feature_description, module_name, function_signature, test_code fields)
3. Write 5 initial test cases covering basic scenarios (e.g., LRU cache, rate limiter, string validator, stack data structure, simple parser)

**Dependencies**: None

**Phase 2: Test Execution Infrastructure**
4. Create bash script skeleton that reads test_cases.json and iterates through cases
5. Implement Python test execution logic: write generated code + test to temp files, run pytest, parse output
6. Test execution with mock artifacts to verify pytest integration works correctly

**Dependencies**: Phase 1 complete (test cases must exist)

**Phase 3: LLM Rubric Evaluation**
7. Create rubric prompt templates for specs (Completeness, Clarity, Testability), plans (Feasibility, Detail Level, Phase Organization), implementations (Actionability, Granularity, Dependencies)
8. Implement Claude sub-agent invocation in bash script using Task tool pattern
9. Test rubric scoring with sample artifacts to validate scoring consistency

**Dependencies**: Phase 2 complete (need artifact handling logic)

**Phase 4: Interactive Workflow**
10. Implement interactive prompts that display feature descriptions and wait for operator to paste artifacts
11. Add artifact validation (check if pasted content matches expected format)
12. Create workspace management (timestamp-based run directories, artifact storage)

**Dependencies**: Phase 3 complete (need full scoring pipeline)

**Phase 5: Results & Reporting**
13. Implement JSON report generation with overall pass rate, per-test results, artifact scores
14. Create baseline storage logic (append to baselines.json with timestamp)
15. Add regression detection (compare current pass rate to previous runs, flag degradation)

**Dependencies**: Phase 4 complete (need full execution to have results)

**Phase 6: Completion**
16. Add remaining 5-10 test cases to reach 10-15 total, covering diverse scenarios
17. Write README documentation with usage instructions, test case format, rubric definitions
18. Run full evaluation to establish initial baseline

**Dependencies**: Phase 5 complete (infrastructure must be working)

---

## **Integration Points**

- **Claude Code Commands**: Evaluation runner prompts human to execute `/spec`, `/plan`, `/implement` commands; doesn't directly invoke them
- **Claude Code Task Tool**: Used for LLM-as-judge rubric scoring via sub-agent invocation from bash script
- **Python Runtime**: `python -m pytest` executes generated code with pytest tests for functional validation
- **Git Repository**: Evaluation results and baselines stored in `.specimin/eval/` (git-tracked for history)
- **Specimin Setup Script**: No integration needed; evaluation is independent of feature setup workflow

---

## **Testing Strategy**

**Unit**: Verify test_cases.json schema validity, check rubric prompt templates are well-formed, validate JSON parsing in bash script, confirm pytest runs with sample test files

**Integration**: Test Python execution with known-good code+test pairs, verify Claude sub-agent rubric scoring returns 1-5 scores, confirm baseline append logic doesn't corrupt JSON

**E2E**: Full evaluation run with 3 test cases: manually run Specimin commands, paste artifacts into runner, verify pytest executes and rubrics score, check report generation and baseline storage

**Edge Cases**: Test execution failures (syntax errors) vs. test assertion failures (logic bugs), malformed artifacts pasted by operator, missing rubric scores from LLM, empty or corrupted baselines.json, missing pytest installation

---

## **Risk Assessment & Mitigation**

**Risk**: Non-deterministic LLM outputs produce valid but different implementations that fail tests
→ **Mitigations**: Design test cases with flexible assertions (test behavior not exact code), use multiple test assertions to allow implementation variance, document expected variability in test case comments

**Risk**: Human operator error (paste wrong artifact, skip test case, corrupt input)
→ **Mitigations**: Add artifact validation (check for markdown headers, detect malformed content), implement "continue from checkpoint" feature to resume interrupted runs, provide clear prompts with example formatting

**Risk**: pytest test execution failures due to syntax errors (broken generated code)
→ **Mitigations**: Distinguish test execution failures from test assertion failures in reports, capture stderr output for debugging, count syntax errors separately from functional failures in pass rate

**Risk**: Claude sub-agent unavailable or returns invalid rubric scores
→ **Mitigations**: Add retry logic for LLM calls, validate score format (1-5 integer), fall back to "N/A" if scoring fails but continue evaluation, document LLM requirements

**Risk**: Baseline file growth degrades performance or becomes unmanageable
→ **Mitigations**: Implement optional `--baseline-limit` flag to keep only last N runs, add rotation logic after 50+ runs, document cleanup procedure in README

**Risk**: Python/pytest not available in evaluation environment
→ **Mitigations**: Add environment check at script start (verify python3 and pytest installed), provide clear installation instructions in README, consider adding requirements.txt for pytest version pinning

**Risk**: Test cases become flaky (especially time-based features like rate limiters)
→ **Mitigations**: Avoid time-dependent test cases in initial suite, use deterministic scenarios (data structures, pure functions), document known flaky tests if added later
