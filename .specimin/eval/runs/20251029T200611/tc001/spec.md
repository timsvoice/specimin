# Feature Specification: LRU Cache

**Objective**: Build an LRU (Least Recently Used) cache data structure that provides O(1) time complexity for both get and put operations, with automatic eviction of least recently used items when capacity is exceeded.

**Context**: LRU caches are fundamental data structures used in many applications including:
- Web browsers for caching recently accessed pages
- Operating systems for memory management
- Database query result caching
- API response caching layers
- Content delivery networks

The LRU eviction policy ensures frequently accessed data remains available while automatically removing stale data, making it ideal for scenarios with limited memory and predictable access patterns.

**Assumptions**:
1. The cache will be used in a single-threaded environment (no concurrent access)
2. Keys can be any hashable type (integers, strings, tuples, etc.)
3. Values can be any Python object
4. The capacity is a positive integer specified at initialization
5. Missing keys should return a sentinel value (None or -1)
6. Both read (get) and write (put) operations count as "usage" for recency tracking
7. Updating an existing key's value should also update its recency

**Constraints**:
- **Performance**: Both get() and put() must operate in O(1) time complexity
- **Space**: O(capacity) space complexity
- **Capacity**: Must strictly enforce the maximum capacity limit
- **Immutability**: Once initialized, capacity cannot be changed
- **Type flexibility**: Support generic key-value pairs without type restrictions

**Acceptance Criteria**:

1. **Initialization**
   - Accept a positive integer capacity parameter
   - Initialize an empty cache

2. **Get Operation**
   - Retrieve value associated with a key in O(1) time
   - Return None or -1 if key doesn't exist
   - Mark the accessed key as most recently used
   - Do not modify cache contents

3. **Put Operation**
   - Insert or update key-value pair in O(1) time
   - If key exists, update value and mark as most recently used
   - If cache is at capacity and key is new, evict least recently used item first
   - Mark the inserted/updated key as most recently used

4. **Eviction Behavior**
   - When cache reaches capacity, adding a new key must evict the LRU item
   - Eviction must maintain O(1) time complexity
   - Only evict when necessary (capacity exceeded by new insertion)

**User Scenarios**:

*Scenario 1: Basic Usage*
```python
cache = LRUCache(capacity=2)
cache.put(1, 'one')
cache.put(2, 'two')
result = cache.get(1)  # Returns 'one'
```

*Scenario 2: Capacity Enforcement*
```python
cache = LRUCache(capacity=2)
cache.put(1, 'one')
cache.put(2, 'two')
cache.put(3, 'three')  # Evicts key 1 (least recently used)
result = cache.get(1)  # Returns None or -1 (evicted)
```

*Scenario 3: Access Updates Recency*
```python
cache = LRUCache(capacity=2)
cache.put(1, 'one')
cache.put(2, 'two')
cache.get(1)           # Makes key 1 most recent
cache.put(3, 'three')  # Evicts key 2 (now least recent)
result = cache.get(2)  # Returns None or -1 (evicted)
```

*Scenario 4: Update Existing Key*
```python
cache = LRUCache(capacity=2)
cache.put(1, 'one')
cache.put(2, 'two')
cache.put(1, 'ONE')    # Updates value and recency
cache.put(3, 'three')  # Evicts key 2
result = cache.get(1)  # Returns 'ONE'
```

**Edge Cases**:

1. **Capacity of 1**
   - Cache can only hold one item
   - Every put operation evicts previous item (if different key)

2. **Missing Keys**
   - get() on non-existent key returns None or -1
   - No error thrown for missing keys

3. **Duplicate Puts**
   - Putting same key multiple times updates value and recency
   - No eviction occurs

4. **Empty Cache**
   - get() on empty cache returns None or -1
   - First put() operation succeeds without eviction

5. **Sequential Access Pattern**
   - Items accessed in order should be evicted in order
   - Verify FIFO-like behavior when no keys are re-accessed

6. **Type Flexibility**
   - Support mixed key types (integers, strings)
   - Support various value types (primitives, objects, None)

**Dependencies**:
- Standard Python library only (no external packages required)
- Python 3.7+ (for guaranteed dict ordering as implementation detail)

**Out of Scope**:
1. Thread safety and concurrent access handling
2. Persistence to disk or serialization
3. Cache statistics (hit rate, miss rate, eviction count)
4. Custom eviction policies (LFU, FIFO, etc.)
5. Time-to-live (TTL) expiration
6. Capacity resizing after initialization
7. Bulk operations (get_many, put_many)
8. Cache clear/reset operation
9. Iterator support for traversing cache contents
10. Deep copying of mutable values
