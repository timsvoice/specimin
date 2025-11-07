# Simple Expression Parser - Implementation Tasks

## Task 1: Create Project Structure
**Objective**: Set up the basic file structure and imports

**Actions**:
1. Create a new Python file (e.g., `expression_parser.py`)
2. Add docstring describing the module
3. Import required standard library modules (if any)

**Acceptance**:
- File exists and can be imported
- Module docstring explains purpose

---

## Task 2: Define Custom Exception
**Objective**: Create a custom exception class for parser errors

**Actions**:
1. Define `ExpressionParserError` class inheriting from `Exception`
2. Add custom `__init__` to accept message and optional position
3. Add `__str__` method to format error with position if available

**Example**:
```python
class ExpressionParserError(Exception):
    def __init__(self, message, position=None):
        self.message = message
        self.position = position
        super().__init__(self._format_message())

    def _format_message(self):
        if self.position is not None:
            return f"{self.message} at position {self.position}"
        return self.message
```

**Acceptance**:
- Exception can be raised and caught
- Position information is included when provided

---

## Task 3: Define Token Class
**Objective**: Create a data structure to represent lexical tokens

**Actions**:
1. Define `Token` class (can use dataclass or simple class)
2. Add fields: `type` (str), `value` (any), `position` (int)
3. Add `__repr__` for debugging

**Token Types**:
- `NUMBER`: Numeric literal
- `PLUS`: + operator
- `MINUS`: - operator
- `MULT`: * operator
- `DIV`: / operator
- `LPAREN`: ( left parenthesis
- `RPAREN`: ) right parenthesis
- `EOF`: End of input

**Acceptance**:
- Token instances can be created
- Token has all required fields
- Token repr is readable

---

## Task 4: Create ExpressionParser Class Skeleton
**Objective**: Set up the main parser class with initialization

**Actions**:
1. Define `ExpressionParser` class
2. Add `__init__` method (takes no arguments per spec)
3. Add placeholder for `evaluate` method

**Example**:
```python
class ExpressionParser:
    def __init__(self):
        """Initialize the expression parser."""
        pass

    def evaluate(self, expression: str) -> int:
        """Evaluate a mathematical expression and return the result."""
        raise NotImplementedError("To be implemented")
```

**Acceptance**:
- Class can be instantiated
- evaluate() method exists (can raise NotImplementedError for now)

---

## Task 5: Implement Tokenizer - Basic Structure
**Objective**: Create the tokenization method framework

**Actions**:
1. Add `_tokenize` method that takes expression string
2. Initialize empty token list
3. Add loop to iterate through expression characters
4. Add position tracking variable
5. Return token list with EOF token at end

**Example**:
```python
def _tokenize(self, expression: str) -> list:
    """Convert expression string into list of tokens."""
    tokens = []
    position = 0

    while position < len(expression):
        char = expression[position]
        # Token recognition will go here
        position += 1

    tokens.append(Token('EOF', None, position))
    return tokens
```

**Acceptance**:
- Method exists and returns a list
- EOF token is always appended

---

## Task 6: Implement Tokenizer - Whitespace Handling
**Objective**: Skip whitespace characters during tokenization

**Actions**:
1. In tokenizer loop, check if current character is whitespace
2. If whitespace, increment position and continue
3. Test with expressions containing spaces

**Acceptance**:
- Expressions with spaces tokenize correctly
- Leading/trailing spaces are handled
- Multiple consecutive spaces are skipped

---

## Task 7: Implement Tokenizer - Single-Character Operators
**Objective**: Recognize and tokenize +, -, *, /, (, ) operators

**Actions**:
1. Add if/elif chain for single-character tokens
2. For each operator character, create appropriate Token
3. Append to token list and increment position

**Example**:
```python
if char == '+':
    tokens.append(Token('PLUS', None, position))
    position += 1
elif char == '-':
    tokens.append(Token('MINUS', None, position))
    position += 1
# ... etc for *, /, (, )
```

**Acceptance**:
- Single operators are tokenized correctly
- Token position matches character position in string
- All six operators (+, -, *, /, (, )) work

---

## Task 8: Implement Tokenizer - Number Recognition
**Objective**: Recognize and tokenize multi-digit integers

**Actions**:
1. Add check for digit characters using `char.isdigit()`
2. When digit found, collect all consecutive digits
3. Convert collected digits to integer
4. Create NUMBER token with integer value
5. Update position to after the number

**Example**:
```python
if char.isdigit():
    start_pos = position
    num_str = ''
    while position < len(expression) and expression[position].isdigit():
        num_str += expression[position]
        position += 1
    tokens.append(Token('NUMBER', int(num_str), start_pos))
```

**Acceptance**:
- Single digit numbers work (e.g., "5")
- Multi-digit numbers work (e.g., "123")
- Number value is stored as integer
- Position points to first digit

---

## Task 9: Implement Tokenizer - Invalid Character Handling
**Objective**: Detect and report invalid characters in expression

**Actions**:
1. Add else clause for unrecognized characters
2. Raise `ExpressionParserError` with descriptive message
3. Include the invalid character and position

**Example**:
```python
else:
    raise ExpressionParserError(
        f"Invalid character '{char}'",
        position
    )
```

**Acceptance**:
- Invalid characters raise ExpressionParserError
- Error message includes the character and position
- Examples: "2 + a", "5 & 3"

---

## Task 10: Test Tokenizer Independently
**Objective**: Verify tokenizer works correctly before building parser

**Actions**:
1. Create test expressions
2. Call `_tokenize()` directly
3. Verify token sequence is correct

**Test Cases**:
- "2 + 3" → [NUMBER(2), PLUS, NUMBER(3), EOF]
- "10 * 5" → [NUMBER(10), MULT, NUMBER(5), EOF]
- "(2 + 3)" → [LPAREN, NUMBER(2), PLUS, NUMBER(3), RPAREN, EOF]
- "  5  " → [NUMBER(5), EOF] (whitespace handling)

**Acceptance**:
- All test cases produce expected token sequences
- Edge cases work correctly

---

## Task 11: Implement Parser State Management
**Objective**: Set up parser state for traversing tokens

**Actions**:
1. Add `_init_parser` method to initialize parser state
2. Store tokens list in `self.tokens`
3. Initialize `self.position` to 0
4. Initialize `self.current_token` to first token

**Example**:
```python
def _init_parser(self, tokens: list):
    """Initialize parser state with token list."""
    self.tokens = tokens
    self.position = 0
    self.current_token = self.tokens[0]
```

**Acceptance**:
- Parser state variables are set correctly
- Current token points to first token

---

## Task 12: Implement Parser Helper Methods
**Objective**: Create utility methods for token navigation

**Actions**:
1. Implement `_advance()`: Move to next token
2. Implement `_expect(token_type)`: Verify current token type and advance
3. Add error handling for unexpected tokens

**Example**:
```python
def _advance(self):
    """Move to the next token."""
    self.position += 1
    if self.position < len(self.tokens):
        self.current_token = self.tokens[self.position]

def _expect(self, token_type: str):
    """Verify current token is of expected type, then advance."""
    if self.current_token.type != token_type:
        raise ExpressionParserError(
            f"Expected {token_type}, got {self.current_token.type}",
            self.current_token.position
        )
    self._advance()
```

**Acceptance**:
- `_advance()` moves to next token correctly
- `_expect()` raises error for wrong token type
- `_expect()` advances on success

---

## Task 13: Implement _parse_factor() Method
**Objective**: Parse highest precedence level (numbers and parentheses)

**Actions**:
1. Define `_parse_factor()` method
2. Handle NUMBER token: extract value and advance
3. Handle LPAREN token: recursively call `_parse_expression()`, expect RPAREN
4. Raise error for unexpected tokens

**Example**:
```python
def _parse_factor(self) -> int:
    """Parse a factor: NUMBER | '(' expression ')'"""
    token = self.current_token

    if token.type == 'NUMBER':
        self._advance()
        return token.value
    elif token.type == 'LPAREN':
        self._advance()
        result = self._parse_expression()
        self._expect('RPAREN')
        return result
    else:
        raise ExpressionParserError(
            f"Unexpected token: {token.type}",
            token.position
        )
```

**Acceptance**:
- Single numbers are parsed correctly
- Parenthesized expressions are parsed recursively
- Missing closing parenthesis raises error
- Unexpected tokens raise error

---

## Task 14: Implement _parse_term() Method
**Objective**: Parse multiplication and division operations

**Actions**:
1. Define `_parse_term()` method
2. Parse left factor
3. Loop while current token is MULT or DIV
4. For each operator, parse right factor and apply operation
5. Handle division by zero error

**Example**:
```python
def _parse_term(self) -> int:
    """Parse a term: factor (('*' | '/') factor)*"""
    result = self._parse_factor()

    while self.current_token.type in ('MULT', 'DIV'):
        op = self.current_token.type
        self._advance()
        right = self._parse_factor()

        if op == 'MULT':
            result = result * right
        elif op == 'DIV':
            if right == 0:
                raise ExpressionParserError(
                    "Division by zero",
                    self.current_token.position
                )
            result = int(result / right)

    return result
```

**Acceptance**:
- Multiplication works: "3 * 4" → 12
- Division works: "20 / 4" → 5
- Multiple operations work: "20 / 4 / 2" → 2 (left-to-right)
- Division by zero raises error
- Integer division truncates: "7 / 2" → 3

---

## Task 15: Implement _parse_expression() Method
**Objective**: Parse addition and subtraction operations (lowest precedence)

**Actions**:
1. Define `_parse_expression()` method
2. Parse left term
3. Loop while current token is PLUS or MINUS
4. For each operator, parse right term and apply operation

**Example**:
```python
def _parse_expression(self) -> int:
    """Parse an expression: term (('+' | '-') term)*"""
    result = self._parse_term()

    while self.current_token.type in ('PLUS', 'MINUS'):
        op = self.current_token.type
        self._advance()
        right = self._parse_term()

        if op == 'PLUS':
            result = result + right
        elif op == 'MINUS':
            result = result - right

    return result
```

**Acceptance**:
- Addition works: "2 + 3" → 5
- Subtraction works: "10 - 4" → 6
- Multiple operations work: "10 - 5 - 2" → 3 (left-to-right)
- Negative results work: "5 - 10" → -5

---

## Task 16: Implement Main evaluate() Method
**Objective**: Wire up tokenizer and parser into public API

**Actions**:
1. Implement `evaluate()` method
2. Validate input is not empty
3. Call `_tokenize()` to get tokens
4. Call `_init_parser()` to set up state
5. Call `_parse_expression()` to parse and evaluate
6. Verify EOF token is reached
7. Return result

**Example**:
```python
def evaluate(self, expression: str) -> int:
    """Evaluate a mathematical expression and return the integer result."""
    # Validate input
    if not expression or not expression.strip():
        raise ExpressionParserError("Empty expression")

    # Tokenize
    tokens = self._tokenize(expression)

    # Parse
    self._init_parser(tokens)
    result = self._parse_expression()

    # Verify we consumed all tokens
    if self.current_token.type != 'EOF':
        raise ExpressionParserError(
            f"Unexpected token after expression: {self.current_token.type}",
            self.current_token.position
        )

    return result
```

**Acceptance**:
- Empty expressions raise error
- Valid expressions return correct result
- Extra tokens after expression raise error

---

## Task 17: Test Basic Operations
**Objective**: Verify each operator works in isolation

**Actions**:
1. Test addition: "2 + 3" → 5
2. Test subtraction: "10 - 4" → 6
3. Test multiplication: "5 * 3" → 15
4. Test division: "20 / 4" → 5

**Acceptance**:
- All four basic operations pass
- Results match expected values

---

## Task 18: Test Operator Precedence
**Objective**: Verify precedence rules are followed

**Actions**:
1. Test "2 + 3 * 4" → 14 (not 20)
2. Test "10 - 2 * 3" → 4 (not 24)
3. Test "6 / 2 + 1" → 4 (not 2)
4. Test "2 * 3 + 4 * 5" → 26

**Acceptance**:
- Multiplication/division evaluated before addition/subtraction
- All test cases pass with correct results

---

## Task 19: Test Parentheses Grouping
**Objective**: Verify parentheses override precedence

**Actions**:
1. Test "(2 + 3) * 4" → 20
2. Test "(10 - 2) * 3" → 24
3. Test "6 / (2 + 1)" → 2
4. Test "((2 + 3) * (4 + 1))" → 25 (nested)

**Acceptance**:
- Parentheses override normal precedence
- Nested parentheses work correctly
- All test cases pass

---

## Task 20: Test Complex Expressions
**Objective**: Verify complex combinations work correctly

**Actions**:
1. Test "2 + 3 * (4 - 1)" → 11
2. Test "(5 + 3) * 2 - 4" → 12
3. Test expression from spec: "(5 + 3) * 2 - 4 / 2" → 14

**Acceptance**:
- Complex expressions with multiple operators and parentheses work
- Results are calculated correctly

---

## Task 21: Test Edge Cases
**Objective**: Verify edge cases are handled properly

**Actions**:
1. Test single number: "42" → 42
2. Test whitespace: "  2  +  3  " → 5
3. Test left-to-right: "10 - 5 - 2" → 3
4. Test negative result: "5 - 10" → -5

**Acceptance**:
- All edge cases pass
- No unexpected errors

---

## Task 22: Test Error Handling
**Objective**: Verify errors are caught and reported clearly

**Actions**:
1. Test empty expression: "" → Error
2. Test division by zero: "5 / 0" → Error
3. Test invalid character: "2 + a" → Error
4. Test unbalanced parentheses: "2 + (3" → Error
5. Test unexpected token: "2 + + 3" → Error

**Acceptance**:
- All invalid inputs raise ExpressionParserError
- Error messages are clear and helpful
- Position information is included where relevant

---

## Task 23: Run Provided Test Suite
**Objective**: Verify implementation passes the official test cases

**Actions**:
1. Locate test file from test_cases.json
2. Run pytest on the test code
3. Fix any failures

**Expected Tests**:
- `test_parser_basic_operations`
- `test_parser_operator_precedence`
- `test_parser_parentheses`
- `test_parser_complex_expressions`

**Acceptance**:
- All provided tests pass
- No errors or failures

---

## Task 24: Code Review and Cleanup
**Objective**: Polish the implementation

**Actions**:
1. Review all code for clarity and consistency
2. Add docstrings to all methods
3. Check for proper error handling
4. Verify code follows Python conventions (PEP 8)
5. Add type hints where helpful
6. Remove any debug prints or unused code

**Acceptance**:
- Code is clean and well-documented
- No TODO comments remain
- Code follows best practices

---

## Task 25: Create Usage Examples
**Objective**: Document how to use the parser

**Actions**:
1. Add module-level docstring with examples
2. Show basic usage
3. Show error handling

**Example**:
```python
"""
Simple mathematical expression parser and evaluator.

Usage:
    parser = ExpressionParser()
    result = parser.evaluate("2 + 3 * 4")  # Returns 14

    try:
        result = parser.evaluate("5 / 0")
    except ExpressionParserError as e:
        print(f"Error: {e}")
"""
```

**Acceptance**:
- Usage examples are clear and accurate
- Module is well-documented

---

## Summary

This implementation follows a systematic approach:
1. **Tasks 1-4**: Project setup and data structures
2. **Tasks 5-10**: Tokenizer implementation and testing
3. **Tasks 11-16**: Parser implementation (bottom-up)
4. **Tasks 17-23**: Comprehensive testing
5. **Tasks 24-25**: Polish and documentation

Each task is atomic, testable, and builds on previous tasks. The implementation can be verified incrementally, ensuring correctness at each stage.
