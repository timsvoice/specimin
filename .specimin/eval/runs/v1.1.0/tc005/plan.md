# Implementation Plan: Simple Expression Parser

## Overview

Implement a mathematical expression parser using a **recursive descent parser** approach. This involves three stages: tokenization (converting string to tokens), parsing (building an abstract syntax tree while respecting precedence), and evaluation (computing the result from the tree).

## Data Structures

### Primary Structure: Token

A token represents a single unit in the expression.

```python
class Token:
    type: TokenType  # NUMBER, PLUS, MINUS, MULTIPLY, DIVIDE, LPAREN, RPAREN, EOF
    value: any       # integer value for NUMBER tokens, None for operators
```

**Rationale**: Separating tokenization from parsing simplifies error handling and makes the parser easier to test and debug.

### Supporting Structures

**TokenType Enum**: Defines all possible token types
- NUMBER, PLUS, MINUS, MULTIPLY, DIVIDE, LPAREN, RPAREN, EOF

**Expression Tree Nodes** (implicit):
- The parser will use the call stack to implicitly build an expression tree
- Each parsing function represents a level of precedence
- This eliminates the need for explicit tree node classes

## Algorithm Approach

### Tokenization (Lexical Analysis)

**Algorithm**: Single-pass scan with lookahead

```
1. Initialize position to 0
2. While position < len(expression):
   a. Skip whitespace
   b. If digit: scan complete number
   c. If operator: create operator token
   d. If parenthesis: create paren token
   e. If invalid character: raise ValueError
3. Append EOF token
```

**Time Complexity**: O(n) - single pass through expression

### Parsing (Syntax Analysis)

**Algorithm**: Recursive Descent Parser with precedence climbing

Use a hierarchy of parsing functions corresponding to operator precedence:

```
parse_expression()     # Entry point
  └─ parse_addition()  # Handles + and - (lowest precedence)
      └─ parse_multiplication()  # Handles * and / (higher precedence)
          └─ parse_primary()  # Handles numbers and parentheses (highest)
```

**Precedence Rules**:
1. **Primary** (highest): Numbers, parenthesized expressions
2. **Multiplication/Division**: *, /
3. **Addition/Subtraction** (lowest): +, -

**Parsing Logic**:

```
parse_expression():
    return parse_addition()

parse_addition():
    left = parse_multiplication()
    while current_token is + or -:
        operator = current_token
        advance()
        right = parse_multiplication()
        left = apply(operator, left, right)
    return left

parse_multiplication():
    left = parse_primary()
    while current_token is * or /:
        operator = current_token
        advance()
        right = parse_primary()
        left = apply(operator, left, right)
    return left

parse_primary():
    if current_token is NUMBER:
        value = current_token.value
        advance()
        return value
    elif current_token is LPAREN:
        advance()  # consume (
        result = parse_addition()  # recursively parse inner expression
        expect(RPAREN)  # must have matching )
        advance()  # consume )
        return result
    else:
        raise SyntaxError
```

**Time Complexity**: O(n) - each token processed once

**Space Complexity**: O(d) - call stack depth equals nesting depth

### Evaluation

**Algorithm**: Evaluate during parsing (single-pass)

Instead of building a separate tree and then evaluating it, we evaluate expressions as we parse them. Each parsing function returns a computed integer value.

**Time Complexity**: O(n) - evaluation happens during parsing

## Implementation Phases

### Phase 1: Foundation

**Tasks**:
1. Create project structure (src/expression_parser.py, test/test_expression_parser.py)
2. Define TokenType enum
3. Define Token class
4. Implement basic ExpressionParser class skeleton
5. Set up pytest configuration

**Deliverable**: Project scaffold with empty classes

### Phase 2: Tokenization

**Tasks**:
1. Implement tokenize() method
2. Handle number scanning (multi-digit integers)
3. Handle operator and parenthesis recognition
4. Handle whitespace skipping
5. Handle invalid characters with clear errors
6. Add EOF token

**Tests**:
- Test single-digit numbers
- Test multi-digit numbers
- Test all operators
- Test parentheses
- Test whitespace handling
- Test invalid characters

**Deliverable**: Working tokenizer that converts strings to token lists

### Phase 3: Core Parsing and Evaluation

**Tasks**:
1. Implement parse_primary() - handles numbers and parentheses
2. Implement parse_multiplication() - handles * and /
3. Implement parse_addition() - handles + and -
4. Implement evaluate() - entry point that calls tokenize and parse
5. Implement division by zero check
6. Implement operator application logic

**Tests**:
- Test single numbers
- Test simple addition/subtraction
- Test simple multiplication/division
- Test operator precedence
- Test parentheses overriding precedence
- Test nested parentheses
- Test division by zero

**Deliverable**: Fully functional parser that handles all valid expressions

### Phase 4: Error Handling and Edge Cases

**Tasks**:
1. Implement unbalanced parentheses detection
2. Implement missing operator detection
3. Implement unexpected token detection
4. Implement empty expression handling
5. Add detailed error messages with context
6. Handle edge cases (single number, deeply nested parens)

**Tests**:
- Test unbalanced parentheses (both directions)
- Test missing operators
- Test adjacent operators
- Test empty expressions
- Test expressions starting/ending with operators
- Test deeply nested valid expressions

**Deliverable**: Robust parser with comprehensive error handling

## Key Considerations

### Design Decisions

**Why Recursive Descent over Shunting Yard?**
- Recursive descent is more intuitive and easier to understand
- Natural mapping between grammar rules and code
- Easier to extend with new operators or features
- Call stack handles precedence automatically

**Why Evaluate During Parsing?**
- Simpler implementation (no separate tree structure)
- Better performance (single pass)
- Sufficient for this use case (no need to inspect/optimize tree)

**Why Integer Division?**
- Spec requirement: integers only
- Python's // operator truncates toward negative infinity
- Use int(a / b) to truncate toward zero (more intuitive for users)

### Error Handling Strategy

**Exception Types**:
- `ValueError`: Invalid characters, empty expressions
- `SyntaxError`: Malformed expressions (unbalanced parens, missing operators)
- `ZeroDivisionError`: Division by zero

**Error Messages Should Include**:
- What went wrong
- Where it went wrong (position in expression if possible)
- What was expected vs what was found

### Extensibility

The recursive descent approach makes it easy to add:
- New operators: Add to tokenizer and create/modify parsing functions
- Unary operators: Add parse_unary() between parse_primary() and parse_multiplication()
- Functions: Add function call parsing in parse_primary()
- Variables: Add variable lookup in parse_primary()

## Testing Strategy

### Unit Tests

**Tokenizer Tests** (isolated):
- Test tokenization of various expressions
- Verify correct token types and values
- Test error cases

**Parser Tests** (integration):
- Test evaluation results of expressions
- Cover all requirement scenarios (R01-R12)
- Test edge cases and error conditions

### Test Organization

**Positive Tests**:
- Basic operations (R01)
- Multiple same-precedence operations (R02)
- Precedence rules (R03)
- Parentheses (R04)
- Nested parentheses (R05)
- Whitespace handling (R06)
- Integer division (R12)

**Negative Tests**:
- Division by zero (R07)
- Invalid syntax (R08)
- Unbalanced parentheses (R09)
- Invalid characters (R10)
- Empty expressions (R11)

### Test Coverage Goals

- 100% line coverage
- All error paths tested
- All edge cases covered
- All spec requirements validated

## Performance Analysis

### Time Complexity

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Tokenization | O(n) | Single pass through string |
| Parsing | O(n) | Each token processed once |
| Overall | O(n) | Linear in expression length |

### Space Complexity

| Component | Complexity | Notes |
|-----------|-----------|-------|
| Token list | O(n) | One token per symbol |
| Call stack | O(d) | d = max nesting depth |
| Overall | O(n + d) | Typically d << n |

### Optimization Opportunities (Future)

- Avoid creating token list (parse directly from string)
- Memoization for repeated subexpressions
- Compile expressions to bytecode for repeated evaluation
- But for this spec: premature optimization, keep it simple
