**Objective**
Create a Python calculator module providing basic arithmetic operations: addition, subtraction, multiplication, and division.

**Context**
A reusable calculator module is needed to perform fundamental arithmetic operations with consistent behavior and error handling across the application.

**Assumptions**
- Module will be imported and used programmatically (not a CLI/GUI application)
- Operations are performed on two operands at a time
- Standard Python integer arithmetic rules apply
- Module can be extended with additional operations in the future

**Constraints**
- Must handle integer values only
- Must validate input types strictly (no automatic type conversion)
- Division by zero must return None (not raise exception)
- Module must be self-contained with no external dependencies

**Acceptance Criteria**
- Module provides four functions: add(), subtract(), multiply(), divide()
- Each function accepts exactly two integer parameters
- Functions return integer results (division uses integer division)
- Non-integer inputs raise TypeError with descriptive message
- Division by zero returns None instead of raising exception
- All functions are pure (no side effects, same inputs produce same outputs)

**User Scenarios**
1. **Basic arithmetic**: Call `add(5, 3)` → Returns `8`
2. **Subtraction**: Call `subtract(10, 4)` → Returns `6`
3. **Multiplication**: Call `multiply(7, 6)` → Returns `42`
4. **Division**: Call `divide(20, 4)` → Returns `5`
5. **Division by zero**: Call `divide(10, 0)` → Returns `None`
6. **Invalid input**: Call `add(5, "3")` → Raises `TypeError`
7. **Negative numbers**: Call `subtract(5, 10)` → Returns `-5`

**Edge Cases**
- Division by zero returns None
- Integer division truncates toward zero (e.g., divide(7, 2) returns 3)
- Negative operands handled correctly
- Very large integers (beyond typical int range if applicable)
- TypeError raised for float, string, None, or other non-integer types

**Dependencies**
None - uses only Python standard library

**Out of Scope**
- Floating-point arithmetic
- Complex numbers or other numeric types
- Chaining operations or expression parsing
- GUI or command-line interface
- History or memory functions
- Advanced operations (power, modulo, square root, etc.)
- Automatic type conversion/coercion
