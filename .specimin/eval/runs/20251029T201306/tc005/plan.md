# Simple Expression Parser - Implementation Plan

## Overview
Build a mathematical expression parser using a two-pass approach: tokenization followed by recursive descent parsing with operator precedence climbing.

## Algorithm Selection

### Considered Approaches

**Option 1: Shunting Yard Algorithm**
- Converts infix to postfix (RPN) then evaluates
- Pros: Clean separation of parsing and evaluation, well-documented
- Cons: Two passes (conversion + evaluation), harder to provide error messages with context

**Option 2: Recursive Descent Parser**
- Directly evaluates while parsing using recursive functions
- Pros: Simple to understand, natural precedence handling, easy error reporting
- Cons: Can be verbose with multiple functions

**Option 3: Operator Precedence Climbing**
- Iterative approach with precedence-based parsing
- Pros: Efficient, compact code, good balance of clarity and performance
- Cons: Slightly harder to understand initially

**Selected Approach: Recursive Descent Parser**
- Best balance of clarity, maintainability, and error handling
- Natural mapping to grammar rules
- Easier to extend if needed
- Performance is O(n) which meets requirements

## Architecture

### Component Structure

```
ExpressionParser
├── __init__(capacity)
├── evaluate(expression: str) -> int
│   ├── _tokenize(expression: str) -> List[Token]
│   ├── _parse() -> int
│   │   ├── _parse_expression() -> int
│   │   ├── _parse_term() -> int
│   │   └── _parse_factor() -> int
│   └── error handling
```

### Grammar Definition

The parser will implement this grammar:
```
expression := term (('+' | '-') term)*
term       := factor (('*' | '/') factor)*
factor     := NUMBER | '(' expression ')'
```

This grammar naturally encodes operator precedence:
- Expressions handle lowest precedence (+, -)
- Terms handle higher precedence (*, /)
- Factors handle highest precedence (numbers and parentheses)

## Data Structures

### Token Class
```python
class Token:
    type: str      # 'NUMBER', 'PLUS', 'MINUS', 'MULT', 'DIV', 'LPAREN', 'RPAREN', 'EOF'
    value: any     # Integer for NUMBER, None for operators
    position: int  # Position in original string (for error messages)
```

### Parser State
```python
self.tokens: List[Token]  # Tokenized input
self.position: int        # Current position in token list
self.current_token: Token # Current token being processed
```

## Implementation Steps

### Phase 1: Tokenizer
1. Create Token class to represent lexical elements
2. Implement `_tokenize()` method:
   - Scan through expression string character by character
   - Skip whitespace
   - Recognize multi-digit numbers
   - Recognize operators and parentheses
   - Track position for error reporting
   - Append EOF token at end
3. Add validation for invalid characters

### Phase 2: Parser Infrastructure
1. Implement parser state management:
   - `self.tokens` to store token list
   - `self.position` to track current position
   - `self.current_token` for lookahead
2. Implement helper methods:
   - `_advance()`: Move to next token
   - `_peek()`: Look at current token without consuming
   - `_expect(token_type)`: Consume token and verify type
3. Add error reporting with position context

### Phase 3: Recursive Descent Parser
1. Implement `_parse_factor()`:
   - Handle NUMBER tokens (base case)
   - Handle parenthesized expressions
   - Validate closing parentheses
2. Implement `_parse_term()`:
   - Parse left factor
   - Loop while current token is * or /
   - Parse right factor and apply operation
   - Handle division by zero
3. Implement `_parse_expression()`:
   - Parse left term
   - Loop while current token is + or -
   - Parse right term and apply operation
4. Implement main `_parse()` entry point:
   - Call `_parse_expression()`
   - Verify EOF token is reached
   - Return final result

### Phase 4: Main API
1. Implement `evaluate()` method:
   - Validate input (not empty)
   - Call `_tokenize()`
   - Initialize parser state
   - Call `_parse()`
   - Return result
2. Wrap with comprehensive error handling

### Phase 5: Error Handling
1. Define custom exception: `ExpressionParserError`
2. Add validation checks:
   - Empty expression
   - Invalid characters in tokenizer
   - Unexpected tokens in parser
   - Unbalanced parentheses
   - Division by zero
   - Incomplete expressions
3. Provide clear error messages with position information

## Key Implementation Considerations

### Operator Precedence
- Handled structurally through grammar levels
- Lower precedence operators call higher precedence parsers
- No need for explicit precedence table

### Left-to-Right Associativity
- Achieved through iterative loops in term and expression parsers
- Example: `10 - 5 - 2` is parsed as `(10 - 5) - 2 = 3`

### Integer Division
- Python 3's `/` operator returns float
- Use `//` for integer division? No - spec says division returns integer
- Use `int(a / b)` to truncate toward zero
- Be careful: `//` truncates toward negative infinity, but `/` truncated gives truncation toward zero

### Whitespace Handling
- Strip all whitespace during tokenization
- Makes parser logic cleaner

### Token Position Tracking
- Maintain original position for each token
- Enables precise error messages

## Testing Strategy

### Unit Tests
1. **Tokenizer Tests**:
   - Valid expressions with all operators
   - Whitespace handling
   - Multi-digit numbers
   - Invalid characters

2. **Parser Tests**:
   - Single operations (each operator)
   - Operator precedence
   - Parentheses grouping
   - Nested parentheses
   - Left-to-right associativity

3. **Edge Case Tests**:
   - Single number
   - Division by zero
   - Empty expression
   - Unbalanced parentheses
   - Invalid syntax

4. **Integration Tests**:
   - Complex expressions from test_cases.json
   - Real-world calculator scenarios

### Test-Driven Development Approach
1. Write tests first based on acceptance criteria
2. Implement tokenizer, verify with tokenizer tests
3. Implement parser components incrementally
4. Verify each grammar level works before moving up
5. Add edge case handling as tests fail

## Performance Characteristics

- **Time Complexity**: O(n) - single pass tokenization, single pass parsing
- **Space Complexity**: O(n) - token list storage
- **No Recursion Depth Issues**: Depth limited by expression nesting (parentheses)

## Example Walkthrough

Expression: `"2 + 3 * 4"`

**Tokenization**:
```
[NUMBER(2), PLUS, NUMBER(3), MULT, NUMBER(4), EOF]
```

**Parsing**:
```
parse_expression()
  parse_term()
    parse_factor() -> 2
    return 2
  see PLUS, continue
  parse_term()
    parse_factor() -> 3
    see MULT, continue
    parse_factor() -> 4
    return 3 * 4 = 12
  return 2 + 12 = 14
```

Result: 14 ✓

## Risk Mitigation

1. **Risk**: Complex recursion leads to stack overflow
   - **Mitigation**: Grammar is bounded by expression nesting depth
   - **Fallback**: Could add maximum depth limit if needed

2. **Risk**: Division semantics unclear (floor vs truncate)
   - **Mitigation**: Use `int(a / b)` for truncation toward zero
   - **Validation**: Add specific tests for negative division

3. **Risk**: Error messages are unclear
   - **Mitigation**: Track token positions, provide context in errors
   - **Testing**: Validate error message quality in tests

4. **Risk**: Tokenizer mishandles edge cases
   - **Mitigation**: Comprehensive tokenizer tests before parser
   - **Validation**: Test boundary conditions explicitly
