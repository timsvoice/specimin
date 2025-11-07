# Simple Expression Parser - Specification

**Objective**: Build a mathematical expression parser and evaluator that can parse and compute the result of arithmetic expressions containing integers, basic operators (+, -, *, /), and parentheses while respecting standard operator precedence rules.

**Context**: Mathematical expression parsing is a fundamental problem in computer science with applications in calculators, spreadsheets, scripting languages, and configuration systems. This parser will provide a lightweight, reliable solution for evaluating arithmetic expressions without requiring external libraries or complex dependencies.

**Assumptions**:
- Input expressions are strings containing valid mathematical notation
- Operations are performed on integers (whole numbers)
- Division is integer division (truncates toward zero)
- Expressions contain only the four basic arithmetic operators: +, -, *, /
- Whitespace in expressions is allowed and should be ignored
- Single-threaded execution (no concurrent access)
- Expressions are well-formed (parentheses are balanced)
- Input expressions are reasonably sized (not pathologically large)

**Constraints**:
- **Time Complexity**: O(n) where n is the length of the expression string
- **Space Complexity**: O(n) for parsing structures (stack-based approach)
- **Operator Precedence**: Standard mathematical precedence (* and / before + and -)
- **Associativity**: Left-to-right for operators of equal precedence
- **Error Handling**: Strict validation with clear error messages for invalid inputs
- **No External Dependencies**: Use only standard library features

**Acceptance Criteria**:
1. Successfully evaluates expressions with single operations (e.g., "2 + 3" returns 5)
2. Correctly applies operator precedence (e.g., "2 + 3 * 4" returns 14, not 20)
3. Supports parentheses to override precedence (e.g., "(2 + 3) * 4" returns 20)
4. Handles nested parentheses correctly (e.g., "2 + (3 * (4 - 1))" returns 11)
5. Ignores whitespace in expressions (e.g., "2+3" and "2 + 3" are equivalent)
6. Performs integer division (e.g., "7 / 2" returns 3)
7. Handles negative results (e.g., "5 - 10" returns -5)
8. Raises clear errors for malformed expressions (unbalanced parentheses, invalid characters, etc.)
9. Raises clear errors for division by zero
10. All four basic operators (+, -, *, /) work correctly

**User Scenarios**:

*Scenario 1: Basic Calculator Usage*
1. User creates an ExpressionParser instance
2. User calls evaluate() with a simple expression "10 + 5"
3. Parser returns the integer result 15

*Scenario 2: Complex Expression Evaluation*
1. User creates an ExpressionParser instance
2. User calls evaluate() with a complex expression "(5 + 3) * 2 - 4 / 2"
3. Parser tokenizes the expression
4. Parser builds an evaluation structure respecting precedence and parentheses
5. Parser computes and returns the result 14

*Scenario 3: Error Handling*
1. User creates an ExpressionParser instance
2. User calls evaluate() with an invalid expression "2 + + 3"
3. Parser detects the syntax error
4. Parser raises an exception with a descriptive error message

**Edge Cases**:
1. **Single number**: "42" should return 42
2. **Multiple operations of same precedence**: "10 - 5 - 2" should return 3 (left-to-right)
3. **Nested parentheses**: "((2 + 3) * (4 + 1))" should return 25
4. **Division by zero**: "5 / 0" should raise an error
5. **Whitespace handling**: "  2  +  3  " should return 5
6. **Negative results**: "5 - 10" should return -5
7. **Negative numbers**: "-5 + 3" (if supported) or explicit "0 - 5 + 3"
8. **Empty expression**: "" should raise an error
9. **Unbalanced parentheses**: "2 + (3" should raise an error
10. **Invalid characters**: "2 + a" should raise an error
11. **Multiple divisions**: "20 / 4 / 2" should return 2 (left-to-right)

**Dependencies**:
- Python standard library only (no external packages)
- Expected to work with Python 3.7+

**Out of Scope**:
- Floating-point arithmetic (only integers)
- Exponentials, modulo, or other operators beyond +, -, *, /
- Variables or symbolic computation
- Implicit multiplication (e.g., "2(3)" should be "2 * (3)")
- Unary operators as part of numbers (e.g., "-5" as a literal; use "0 - 5" instead)
- Trigonometric or other mathematical functions
- Expression optimization or simplification
- Multi-threaded or concurrent parsing
- Parsing performance for extremely large expressions (megabytes of text)
