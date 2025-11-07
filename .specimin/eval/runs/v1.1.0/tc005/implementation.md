# Implementation Tasks: Simple Expression Parser

**Overview**: Build a recursive descent parser for mathematical expressions with three phases: tokenization, parsing with precedence handling, and evaluation.

**Total Tasks**: 52
**Phases**: 4

---

## Phase 1: Foundation

**Dependencies**: None
**Parallel Opportunities**: 0

- [ ] T001 Create project structure directory src/ (R01)
- [ ] T002 Create project structure directory test/ (R01)
- [ ] T003 Create empty file src/expression_parser.py (R01)
- [ ] T004 Create empty file test/test_expression_parser.py (R01)
- [ ] T005 Define TokenType enum in src/expression_parser.py with values: NUMBER, PLUS, MINUS, MULTIPLY, DIVIDE, LPAREN, RPAREN, EOF (R01)
- [ ] T006 Define Token class in src/expression_parser.py with fields: type and value (R01)
- [ ] T007 Create ExpressionParser class skeleton in src/expression_parser.py (R01)
- [ ] T008 Add __init__ method to ExpressionParser class (R01)
- [ ] T009 Create pytest configuration file pytest.ini in project root (R01)

---

## Phase 2: Tokenization

**Dependencies**: Phase 1 complete
**Parallel Opportunities**: 0

- [ ] T010 Write test for tokenizing single-digit number in test/test_expression_parser.py (R01)
- [ ] T011 Verify test fails for single-digit number tokenization
- [ ] T012 Implement tokenize() method skeleton in src/expression_parser.py (R01)
- [ ] T013 Implement position tracking and initialization in tokenize() (R01)
- [ ] T014 Implement single-digit number scanning in tokenize() (R01)
- [ ] T015 Verify test passes for single-digit number tokenization

- [ ] T016 Write test for tokenizing multi-digit numbers in test/test_expression_parser.py (R01)
- [ ] T017 Verify test fails for multi-digit number tokenization
- [ ] T018 Implement multi-digit number scanning logic in tokenize() (R01)
- [ ] T019 Verify test passes for multi-digit number tokenization

- [ ] T020 Write test for tokenizing all operators (+, -, *, /) in test/test_expression_parser.py (R01, R03)
- [ ] T021 Verify test fails for operator tokenization
- [ ] T022 Implement operator recognition in tokenize() (R01, R03)
- [ ] T023 Verify test passes for operator tokenization

- [ ] T024 Write test for tokenizing parentheses in test/test_expression_parser.py (R04)
- [ ] T025 Verify test fails for parenthesis tokenization
- [ ] T026 Implement parenthesis recognition in tokenize() (R04)
- [ ] T027 Verify test passes for parenthesis tokenization

- [ ] T028 Write test for whitespace handling in tokenize() in test/test_expression_parser.py (R06)
- [ ] T029 Verify test fails for whitespace handling
- [ ] T030 Implement whitespace skipping in tokenize() (R06)
- [ ] T031 Verify test passes for whitespace handling

- [ ] T032 Write test for invalid character detection in test/test_expression_parser.py (R10)
- [ ] T033 Verify test fails for invalid character detection
- [ ] T034 Implement invalid character error handling in tokenize() (R10)
- [ ] T035 Verify test passes for invalid character detection

- [ ] T036 Write test for EOF token appending in test/test_expression_parser.py (R01)
- [ ] T037 Verify test fails for EOF token
- [ ] T038 Implement EOF token appending in tokenize() (R01)
- [ ] T039 Verify test passes for EOF token

---

## Phase 3: Core Parsing and Evaluation

**Dependencies**: Phase 2 complete
**Parallel Opportunities**: 0

- [ ] T040 Write test for evaluating single number in test/test_expression_parser.py (R01)
- [ ] T041 Verify test fails for single number evaluation
- [ ] T042 Implement parse_primary() method in src/expression_parser.py to handle numbers (R01)
- [ ] T043 Implement current_token property and advance() method in src/expression_parser.py (R01)
- [ ] T044 Implement evaluate() method entry point that calls tokenize in src/expression_parser.py (R01)
- [ ] T045 Verify test passes for single number evaluation

- [ ] T046 Write test for simple addition and subtraction in test/test_expression_parser.py (R01, R02)
- [ ] T047 Verify test fails for addition/subtraction
- [ ] T048 Implement parse_addition() method in src/expression_parser.py (R01, R02)
- [ ] T049 Update evaluate() to call parse_addition() (R01)
- [ ] T050 Verify test passes for addition/subtraction

- [ ] T051 Write test for simple multiplication and division in test/test_expression_parser.py (R01, R03)
- [ ] T052 Verify test fails for multiplication/division
- [ ] T053 Implement parse_multiplication() method in src/expression_parser.py (R01, R03)
- [ ] T054 Update parse_addition() to call parse_multiplication() (R03)
- [ ] T055 Verify test passes for multiplication/division

- [ ] T056 Write test for operator precedence in test/test_expression_parser.py (R03)
- [ ] T057 Verify test fails for operator precedence
- [ ] T058 Verify precedence logic in parse_addition() and parse_multiplication() (R03)
- [ ] T059 Verify test passes for operator precedence

- [ ] T060 Write test for parentheses overriding precedence in test/test_expression_parser.py (R04)
- [ ] T061 Verify test fails for parentheses
- [ ] T062 Implement parentheses handling in parse_primary() (R04)
- [ ] T063 Verify test passes for parentheses

- [ ] T064 Write test for nested parentheses in test/test_expression_parser.py (R05)
- [ ] T065 Verify test fails for nested parentheses
- [ ] T066 Verify recursive parentheses logic in parse_primary() (R05)
- [ ] T067 Verify test passes for nested parentheses

- [ ] T068 Write test for division by zero in test/test_expression_parser.py (R07)
- [ ] T069 Verify test fails for division by zero
- [ ] T070 Implement division by zero check in parse_multiplication() (R07)
- [ ] T071 Verify test passes for division by zero

- [ ] T072 Write test for integer division behavior in test/test_expression_parser.py (R12)
- [ ] T073 Verify test fails for integer division
- [ ] T074 Implement integer division truncation in parse_multiplication() (R12)
- [ ] T075 Verify test passes for integer division

---

## Phase 4: Error Handling and Edge Cases

**Dependencies**: Phase 3 complete
**Parallel Opportunities**: 0

- [ ] T076 Write test for unbalanced parentheses (missing close) in test/test_expression_parser.py (R09)
- [ ] T077 Verify test fails for unbalanced parentheses
- [ ] T078 Implement expect() method to check for required tokens in src/expression_parser.py (R09)
- [ ] T079 Verify test passes for unbalanced parentheses

- [ ] T080 Write test for unbalanced parentheses (missing open) in test/test_expression_parser.py (R09)
- [ ] T081 Verify test fails for extra closing parenthesis
- [ ] T082 Implement unexpected token detection in parse_primary() (R09)
- [ ] T083 Verify test passes for extra closing parenthesis

- [ ] T084 Write test for missing operators between numbers in test/test_expression_parser.py (R08)
- [ ] T085 Verify test fails for missing operators
- [ ] T086 Implement unexpected token error in parse methods (R08)
- [ ] T087 Verify test passes for missing operators

- [ ] T088 Write test for adjacent operators in test/test_expression_parser.py (R08)
- [ ] T089 Verify test fails for adjacent operators
- [ ] T090 Implement operator validation in parse methods (R08)
- [ ] T091 Verify test passes for adjacent operators

- [ ] T092 Write test for empty expression in test/test_expression_parser.py (R11)
- [ ] T093 Verify test fails for empty expression
- [ ] T094 Implement empty expression check in evaluate() (R11)
- [ ] T095 Verify test passes for empty expression

- [ ] T096 Write test for whitespace-only expression in test/test_expression_parser.py (R11)
- [ ] T097 Verify test fails for whitespace-only expression
- [ ] T098 Implement whitespace-only detection in tokenize() or evaluate() (R11)
- [ ] T099 Verify test passes for whitespace-only expression

- [ ] T100 Write test for expression starting with operator in test/test_expression_parser.py (R08)
- [ ] T101 Verify test fails for starting operator
- [ ] T102 Implement starting operator detection in parse_primary() (R08)
- [ ] T103 Verify test passes for starting operator

- [ ] T104 Write test for expression ending with operator in test/test_expression_parser.py (R08)
- [ ] T105 Verify test fails for ending operator
- [ ] T106 Implement ending operator detection in parse methods (R08)
- [ ] T107 Verify test passes for ending operator

- [ ] T108 Write test for deeply nested parentheses in test/test_expression_parser.py (R05)
- [ ] T109 Verify test fails for deeply nested parentheses
- [ ] T110 Verify recursive depth handling works correctly (R05)
- [ ] T111 Verify test passes for deeply nested parentheses

- [ ] T112 Write test for complex expressions combining all features in test/test_expression_parser.py (R01-R12)
- [ ] T113 Verify test fails for complex expressions
- [ ] T114 Verify all components work together correctly (R01-R12)
- [ ] T115 Verify test passes for complex expressions

---

## Spec Requirement Mapping

- R01 (Single operator): Tasks T001-T009, T010-T039, T040-T045, T046-T050, T051-T055
- R02 (Multiple same precedence): Tasks T046-T050
- R03 (Operator precedence): Tasks T051-T059
- R04 (Parentheses override): Tasks T060-T063
- R05 (Nested parentheses): Tasks T064-T067, T108-T111
- R06 (Whitespace handling): Tasks T028-T031
- R07 (Division by zero): Tasks T068-T071
- R08 (Invalid syntax): Tasks T084-T091, T100-T107
- R09 (Unbalanced parentheses): Tasks T076-T083
- R10 (Invalid characters): Tasks T032-T035
- R11 (Empty expressions): Tasks T092-T099
- R12 (Integer division): Tasks T072-T075

---

## Critical Dependencies

**Sequential Dependencies**:
1. Tokenization (Phase 2) requires Foundation (Phase 1)
2. Parsing (Phase 3) requires working tokenizer (Phase 2)
3. Error handling (Phase 4) requires core parser (Phase 3)

**Within-Phase Dependencies**:
- Multi-digit numbers require single-digit implementation
- Operators must be tokenized before parsing can use them
- parse_addition() must call parse_multiplication() for precedence
- parse_multiplication() must call parse_primary() for precedence
- Parentheses in parse_primary() must call back to parse_addition() for recursion

**TDD Dependencies**:
- Each "verify test fails" must follow "write test"
- Each "implement" must follow "verify test fails"
- Each "verify test passes" must follow "implement"

---

## Notes

**Implementation Approach**: Recursive descent parser with three levels of precedence (primary, multiplication/division, addition/subtraction). The recursion naturally handles nested parentheses.

**Testing Strategy**: Follow TDD strictly - write test, verify it fails (red), implement feature, verify it passes (green). This ensures all code is driven by tests.

**File Organization**: Keep parser simple with single src/expression_parser.py file containing TokenType enum, Token class, and ExpressionParser class. All tests in single test/test_expression_parser.py file.

**Error Messages**: Include context in error messages where possible (e.g., "Unexpected token '+' at position 5"). This helps with debugging invalid expressions.

**Integer Division**: Use int(a / b) rather than a // b to truncate toward zero (more intuitive: 7/2=3, -7/2=-3).
