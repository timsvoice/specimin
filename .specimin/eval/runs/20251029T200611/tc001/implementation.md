# Implementation Tasks: LRU Cache

## Task 1: Create Node Class

**Objective**: Define the doubly linked list node structure.

**Instructions**:
1. Create a `Node` class with `__init__` method
2. Accept `key` and `value` parameters in constructor
3. Initialize four attributes:
   - `self.key = key`
   - `self.value = value`
   - `self.prev = None`
   - `self.next = None`

**Acceptance Criteria**:
- Node stores both key and value
- Node has prev and next pointers initialized to None
- Constructor accepts exactly two parameters (key, value)

**File**: Create new file or add to existing module

---

## Task 2: Create LRUCache Class Skeleton

**Objective**: Set up the LRUCache class structure and initialization.

**Instructions**:
1. Create `LRUCache` class with `__init__` method
2. Accept `capacity` parameter (positive integer)
3. Initialize three attributes:
   - `self.capacity = capacity`
   - `self.cache = {}` (empty dictionary)
   - Create dummy `self.head = Node(0, 0)`
   - Create dummy `self.tail = Node(0, 0)`
4. Link dummy nodes:
   - `self.head.next = self.tail`
   - `self.tail.prev = self.head`

**Acceptance Criteria**:
- LRUCache accepts capacity parameter
- Cache dictionary is initialized as empty
- Dummy head and tail nodes are created and linked
- No other nodes exist initially

---

## Task 3: Implement _remove_node Helper Method

**Objective**: Create helper to remove a node from the linked list.

**Instructions**:
1. Define `_remove_node(self, node)` method
2. Get references to neighboring nodes:
   - `prev_node = node.prev`
   - `next_node = node.next`
3. Update pointers to bypass the node:
   - `prev_node.next = next_node`
   - `next_node.prev = prev_node`

**Acceptance Criteria**:
- Method accepts a node parameter
- Node is removed from its current position
- Neighboring nodes are properly linked
- Node itself is not modified (remains valid for reuse)
- O(1) time complexity

---

## Task 4: Implement _add_to_head Helper Method

**Objective**: Create helper to add a node right after the dummy head.

**Instructions**:
1. Define `_add_to_head(self, node)` method
2. Get reference to current first node:
   - `first_node = self.head.next`
3. Insert node between head and first_node:
   - `node.next = first_node`
   - `node.prev = self.head`
   - `first_node.prev = node`
   - `self.head.next = node`

**Acceptance Criteria**:
- Node is inserted right after dummy head
- All four pointers are updated correctly
- Previous first node becomes second node
- O(1) time complexity

---

## Task 5: Implement _remove_tail Helper Method

**Objective**: Create helper to identify and remove the LRU node.

**Instructions**:
1. Define `_remove_tail(self)` method
2. Get reference to LRU node:
   - `lru_node = self.tail.prev`
3. Remove it from list:
   - Call `self._remove_node(lru_node)`
4. Return the removed node:
   - `return lru_node`

**Acceptance Criteria**:
- Method returns the node before dummy tail
- Node is removed from the linked list
- Returns the actual node object (not just key/value)
- O(1) time complexity

---

## Task 6: Implement get Method

**Objective**: Retrieve value for a key and update its recency.

**Instructions**:
1. Define `get(self, key)` method
2. Check if key exists:
   - `if key not in self.cache:`
   - `return None` (or `-1` based on preference)
3. If key exists:
   - `node = self.cache[key]`
   - `self._remove_node(node)`
   - `self._add_to_head(node)`
   - `return node.value`

**Acceptance Criteria**:
- Returns None (or -1) for missing keys
- Returns correct value for existing keys
- Moves accessed node to head position
- Does not modify cache size
- O(1) time complexity

---

## Task 7: Implement put Method - Update Case

**Objective**: Handle the case where key already exists in cache.

**Instructions**:
1. Define `put(self, key, value)` method
2. Handle existing key case:
   ```python
   if key in self.cache:
       node = self.cache[key]
       node.value = value
       self._remove_node(node)
       self._add_to_head(node)
       return  # Exit early
   ```

**Acceptance Criteria**:
- Updates value for existing key
- Moves updated node to head position
- Does not change cache size
- Does not trigger eviction
- O(1) time complexity

**Note**: This task only implements the update case. Insertion case comes next.

---

## Task 8: Implement put Method - Insertion Case

**Objective**: Handle the case where a new key is being inserted.

**Instructions**:
1. Continue the `put` method (after the existing key check)
2. Check if eviction is needed:
   ```python
   if len(self.cache) >= self.capacity:
       lru_node = self._remove_tail()
       del self.cache[lru_node.key]
   ```
3. Create and insert new node:
   ```python
   new_node = Node(key, value)
   self.cache[key] = new_node
   self._add_to_head(new_node)
   ```

**Acceptance Criteria**:
- Evicts LRU item when at capacity
- Removes evicted key from both dictionary and linked list
- Creates new node with correct key and value
- Adds new node to both dictionary and head of list
- Maintains cache size ≤ capacity
- O(1) time complexity

---

## Task 9: Add Type Hints and Docstrings

**Objective**: Add documentation and type annotations.

**Instructions**:
1. Add type hints to all methods:
   - `def __init__(self, capacity: int) -> None:`
   - `def get(self, key: Any) -> Any:`
   - `def put(self, key: Any, value: Any) -> None:`
2. Add docstrings to public methods:
   ```python
   def get(self, key):
       """
       Retrieve value for key. Returns None if key not found.
       Marks key as most recently used.

       Time complexity: O(1)
       """
   ```
3. Add class-level docstring explaining the data structure

**Acceptance Criteria**:
- All public methods have type hints
- All public methods have docstrings
- Class has overview docstring
- Documentation mentions O(1) time complexity

---

## Task 10: Create Test File and Basic Tests

**Objective**: Set up testing infrastructure with initial test cases.

**Instructions**:
1. Create test file (e.g., `test_lru_cache.py`)
2. Import pytest and the LRUCache implementation
3. Implement three test functions:
   - `test_lru_cache_basic_operations`: Test get/put on non-full cache
   - `test_lru_cache_eviction`: Test capacity enforcement
   - `test_lru_cache_access_updates_recency`: Test get() updates order

**Acceptance Criteria**:
- All three test functions pass
- Tests match the provided test code structure
- Tests cover basic functionality, eviction, and recency updates

---

## Task 11: Test Edge Cases

**Objective**: Verify correctness for boundary conditions.

**Instructions**:
1. Test capacity of 1:
   ```python
   cache = LRUCache(1)
   cache.put(1, 'a')
   cache.put(2, 'b')  # Should evict key 1
   assert cache.get(1) is None
   assert cache.get(2) == 'b'
   ```
2. Test empty cache:
   ```python
   cache = LRUCache(5)
   assert cache.get(999) is None
   ```
3. Test duplicate puts:
   ```python
   cache = LRUCache(2)
   cache.put(1, 'a')
   cache.put(1, 'b')  # Update
   assert len(cache.cache) == 1
   assert cache.get(1) == 'b'
   ```

**Acceptance Criteria**:
- Capacity 1 works correctly
- Empty cache returns None for get
- Duplicate puts update value without growing size
- No crashes or exceptions

---

## Task 12: Verify Time Complexity

**Objective**: Confirm O(1) performance with large capacity.

**Instructions**:
1. Create a large cache (e.g., capacity = 10000)
2. Perform operations and verify they complete quickly:
   ```python
   import time
   cache = LRUCache(10000)

   start = time.time()
   for i in range(10000):
       cache.put(i, i * 2)
   put_time = time.time() - start

   start = time.time()
   for i in range(10000):
       cache.get(i)
   get_time = time.time() - start

   # Verify times are small and linear in n
   assert put_time < 0.1  # Should be very fast
   assert get_time < 0.1
   ```

**Acceptance Criteria**:
- Large cache operations complete quickly
- Performance scales linearly with operations (O(1) per operation)
- No performance degradation with increased capacity

---

## Task 13: Code Review and Cleanup

**Objective**: Final review and polish of implementation.

**Instructions**:
1. Review all code for:
   - Consistent naming conventions
   - Proper indentation and formatting
   - No unused variables or imports
   - No magic numbers (use self.capacity, not hardcoded values)
2. Verify method ordering:
   - Public methods (get, put) before private methods (_remove_node, etc.)
3. Ensure all tests pass:
   ```bash
   pytest test_lru_cache.py -v
   ```

**Acceptance Criteria**:
- Code follows PEP 8 style guidelines
- All tests pass
- No linting errors
- Code is readable and well-organized

---

## Implementation Checklist

- [ ] Task 1: Node class created
- [ ] Task 2: LRUCache skeleton with initialization
- [ ] Task 3: _remove_node helper implemented
- [ ] Task 4: _add_to_head helper implemented
- [ ] Task 5: _remove_tail helper implemented
- [ ] Task 6: get method implemented
- [ ] Task 7: put method - update case
- [ ] Task 8: put method - insertion case
- [ ] Task 9: Type hints and docstrings added
- [ ] Task 10: Basic tests created and passing
- [ ] Task 11: Edge cases tested
- [ ] Task 12: Time complexity verified
- [ ] Task 13: Code review completed

## Expected File Structure

```
lru_cache.py          # Main implementation
test_lru_cache.py     # Test suite
```

## Estimated Completion Time

- Tasks 1-8: 45-60 minutes (core implementation)
- Tasks 9-13: 30-45 minutes (documentation and testing)
- Total: 75-105 minutes

## Success Criteria

Implementation is complete when:
1. All 13 tasks are completed
2. All provided test cases pass
3. Edge cases are handled correctly
4. O(1) time complexity is maintained
5. Code is documented and clean
