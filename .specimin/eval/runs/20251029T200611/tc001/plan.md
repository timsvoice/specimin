# Implementation Plan: LRU Cache

## Problem Analysis

The challenge is achieving O(1) time complexity for both get and put operations while maintaining LRU ordering. This requires:

1. **Fast lookup**: O(1) key-to-value access
2. **Fast updates**: O(1) recency updates
3. **Fast eviction**: O(1) identification and removal of LRU item

A single data structure cannot satisfy all requirements, necessitating a hybrid approach.

## Data Structure Strategy

### Option 1: HashMap + Doubly Linked List (Recommended)

**Components**:
- **HashMap**: Maps keys to node references for O(1) lookup
- **Doubly Linked List**: Maintains LRU ordering (most recent at head, least recent at tail)

**Advantages**:
- O(1) access via hash map
- O(1) reordering via doubly linked list pointers
- O(1) eviction by removing tail node
- Clean separation of concerns

**Disadvantages**:
- More complex implementation
- Additional memory for list pointers

**Verdict**: Best choice for production-quality implementation.

### Option 2: OrderedDict (Alternative)

**Components**:
- Python's `collections.OrderedDict` with move_to_end()

**Advantages**:
- Simpler implementation
- Built-in ordered dictionary functionality
- Less code to maintain

**Disadvantages**:
- Less educational (hides complexity)
- Slightly less explicit about operations
- Python-specific (not transferable to other languages)

**Verdict**: Acceptable for Python-specific solutions, but less instructive.

## Chosen Approach: HashMap + Doubly Linked List

### Core Components

#### 1. Node Class
```python
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None
```

**Purpose**: Represent cache entries in the doubly linked list
**Why store key?**: Needed during eviction to remove from hash map

#### 2. LRUCache Class

**Attributes**:
- `capacity`: Maximum cache size
- `cache`: Dictionary mapping keys to nodes
- `head`: Dummy node marking list start (most recent)
- `tail`: Dummy node marking list end (least recent)

**Why dummy nodes?**: Simplify edge cases (empty list, single item) by avoiding null checks

### Algorithm Details

#### Initialization
```
1. Store capacity
2. Initialize empty dictionary
3. Create dummy head and tail nodes
4. Link head.next → tail
5. Link tail.prev → head
```

Time: O(1), Space: O(1)

#### Get Operation
```
1. Check if key exists in cache dictionary
2. If not found: return None (or -1)
3. If found:
   a. Retrieve node from dictionary
   b. Remove node from current position
   c. Add node to head (mark as most recent)
   d. Return node.value
```

Time: O(1) for all steps

#### Put Operation
```
1. Check if key exists in cache dictionary
2. If exists:
   a. Retrieve existing node
   b. Update node.value
   c. Remove node from current position
   d. Add node to head (mark as most recent)
3. If not exists:
   a. Check if cache is at capacity
   b. If at capacity:
      - Remove tail node (least recent)
      - Delete from dictionary
   c. Create new node
   d. Add to dictionary
   e. Add node to head (mark as most recent)
```

Time: O(1) for all steps

#### Helper: Remove Node
```
Remove node from its current position in linked list:
1. Get prev_node and next_node
2. prev_node.next = next_node
3. next_node.prev = prev_node
```

Time: O(1)

#### Helper: Add to Head
```
Insert node right after dummy head:
1. node.next = head.next
2. node.prev = head
3. head.next.prev = node
4. head.next = node
```

Time: O(1)

#### Helper: Remove Tail
```
Remove the node before dummy tail:
1. lru_node = tail.prev
2. Remove lru_node from list
3. Return lru_node
```

Time: O(1)

## Implementation Considerations

### 1. Edge Cases
- **Capacity = 1**: Ensure single-item eviction works correctly
- **Empty cache**: get() should return None, not crash
- **Duplicate puts**: Update value without growing size

### 2. Data Integrity
- Keep dictionary and linked list synchronized
- Always remove from both structures during eviction
- Always add to both structures during insertion

### 3. Pointer Management
- Carefully update all four pointers when moving nodes
- Use dummy nodes to avoid null pointer checks
- Ensure circular references are avoided

### 4. Method Extraction
- Extract helper methods for clarity:
  - `_remove_node(node)`: Remove from linked list
  - `_add_to_head(node)`: Insert after head
  - `_remove_tail()`: Get and remove LRU node

### 5. Invariants to Maintain
- Dictionary size = linked list size (excluding dummy nodes)
- Dictionary size ≤ capacity
- Most recent item always follows head
- Least recent item always precedes tail

## Testing Strategy

### Unit Tests
1. **Basic operations**: Single get/put operations
2. **Eviction**: Verify LRU item removed at capacity
3. **Recency updates**: Verify get() updates position
4. **Update operations**: Verify put() on existing key
5. **Edge cases**: Capacity 1, empty cache, missing keys

### Property Tests
1. **Size invariant**: Cache size never exceeds capacity
2. **Ordering invariant**: Most recently used always accessible
3. **Eviction correctness**: LRU item always evicted first

### Performance Tests
1. **Time complexity**: Verify O(1) with large capacity
2. **Space complexity**: Verify O(capacity) space usage

## Complexity Analysis

**Time Complexity**:
- get(): O(1) - hash lookup + linked list manipulation
- put(): O(1) - hash lookup + linked list manipulation + possible eviction

**Space Complexity**:
- O(capacity) - hash map + linked list nodes
- Each entry requires: 1 dict entry + 1 node (key, value, 2 pointers)

## Alternative Implementation Notes

If using OrderedDict:
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```

This is much simpler but less instructive about the underlying mechanics.

## Implementation Priority

1. **Phase 1**: Node class and LRUCache skeleton
2. **Phase 2**: Helper methods (_remove_node, _add_to_head, _remove_tail)
3. **Phase 3**: get() method
4. **Phase 4**: put() method
5. **Phase 5**: Testing and edge case handling
