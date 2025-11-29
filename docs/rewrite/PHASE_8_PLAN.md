# Phase 8: Python Developer Experience Enhancements

## Overview

This phase focuses on adding critical Python developer experience features that will make Scrython more powerful and user-friendly. While the library has excellent API coverage (100% of Scryfall endpoints), it lacks several standard Python features that developers expect.

## Key Features to Implement

1. **Magic Methods** - Enable proper object representation and comparison
2. **Serialization** - Allow easy export/import of objects
3. **Default Rate Limiting** - Built-in rate limiting with opt-out capability
4. **Built-in Caching** - HTTP response caching with TTL
5. **Iteration Support** - Pythonic iteration over results
6. **Convenience Methods** - Common operations as one-liners

---

## Phase 1: Magic Methods (Core UX)

**Location:** `scrython/base.py` (ScrythonRequestHandler)

### Implementation

1. Add `__repr__()` - Developer-friendly representation showing class name and key identifiers
2. Add `__str__()` - User-friendly string (e.g., "Lightning Bolt (LEA)")
3. Add `__eq__()` - Compare by Scryfall ID for cards/sets, by object for others
4. Add `__hash__()` - Hash by Scryfall ID to enable use in sets/dicts

### Example Usage

```python
card = scrython.cards.Named(fuzzy='Lightning Bolt')

# Developer representation
repr(card)  # Named(id='bd8fa327-dd41-4737-8f19-2cf5eb1f7cdd', name='Lightning Bolt')

# User-friendly string
str(card)  # Lightning Bolt (LEA)

# Comparison
card1 == card2  # True if same Scryfall ID

# Use in sets/dicts
unique_cards = set([card1, card2, card3])
card_lookup = {card1: 'owned', card2: 'wanted'}
```

### Testing

- Test `__repr__()` output format for different object types
- Test `__str__()` for cards with/without set info
- Test `__eq__()` with same/different cards, different object types
- Test `__hash__()` consistency and use in sets/dicts

---

## Phase 2: Serialization Methods

**Location:** `scrython/base.py` (ScrythonRequestHandler)

### Implementation

1. Add `to_dict()` - Return copy of `_scryfall_data`
2. Add `to_json(**kwargs)` - Serialize to JSON string with configurable formatting
3. Add `from_dict(cls, data)` classmethod - Construct object from dict (for cache rehydration)
4. For list results: Add `to_list()` to serialize all items in `.data`

### Example Usage

```python
card = scrython.cards.Named(fuzzy='Lightning Bolt')

# Export to dict
card_dict = card.to_dict()

# Export to JSON
card_json = card.to_json(indent=2)

# Save to file
with open('card.json', 'w') as f:
    f.write(card.to_json())

# Load from dict (useful for caching)
card_copy = scrython.cards.Named.from_dict(card_dict)

# Export search results
results = scrython.cards.Search(q='bolt')
all_cards = results.to_list()  # List of dicts
```

### Testing

- Test round-trip serialization (to_dict → from_dict)
- Test JSON formatting options (indent, sort_keys, etc.)
- Test `to_list()` for search results
- Test with different object types (cards, sets, bulk data, etc.)

---

## Phase 3: Default Rate Limiting (with Opt-Out)

**Location:** `scrython/base.py` + new `scrython/rate_limiter.py`

### Implementation

1. Create `RateLimiter` class with configurable limits (default: 10 calls/sec per Scryfall guidelines)
2. Integrate into `ScrythonRequestHandler._fetch()` to enforce by default
3. Add `rate_limit=False` parameter to disable (opt-out design)
4. Use thread-safe implementation (threading.Lock + collections.deque for sliding window)
5. Support custom rate limits: `scrython.cards.Search(q='bolt', rate_limit_per_second=5)`

### Example Usage

```python
# Default: Rate limiting enabled at 10 calls/sec
card = scrython.cards.Named(fuzzy='Lightning Bolt')  # Automatically rate limited

# Opt-out of rate limiting
card = scrython.cards.Named(fuzzy='Lightning Bolt', rate_limit=False)

# Custom rate limit
card = scrython.cards.Search(q='bolt', rate_limit_per_second=5)

# Multiple rapid calls - automatically throttled
for name in card_names:
    card = scrython.cards.Named(fuzzy=name)  # Sleeps as needed
```

### Design Details

**RateLimiter Class:**
```python
class RateLimiter:
    def __init__(self, calls_per_second: float = 10.0):
        self.calls_per_second = calls_per_second
        self.min_interval = 1.0 / calls_per_second
        self.last_call = 0.0
        self.lock = threading.Lock()

    def wait(self):
        """Block until rate limit allows next call."""
        with self.lock:
            now = time.time()
            time_since_last = now - self.last_call
            if time_since_last < self.min_interval:
                sleep_time = self.min_interval - time_since_last
                time.sleep(sleep_time)
            self.last_call = time.time()
```

### Testing

- Test rate limiting enforcement (timing between calls)
- Test opt-out functionality
- Test custom rate limits
- Test thread safety (concurrent requests)
- Test edge cases (first call, rapid calls, etc.)

---

## Phase 4: Built-in Caching Layer

**Location:** New `scrython/cache.py` + integration in `scrython/base.py`

### Implementation

1. Create abstract `CacheBackend` interface
2. Implement `MemoryCache` (in-memory with TTL, using `time.time()` for expiration)
3. Create cache key from (endpoint, params) tuple
4. Integrate into `ScrythonRequestHandler._fetch()` with cache lookup before HTTP request
5. Add initialization option: `scrython.cards.Named(fuzzy='bolt', cache=True, cache_ttl=3600)`
6. Respect cache headers from Scryfall if present
7. Design for future: Abstract interface allows redis/sqlite backends later

### Example Usage

```python
# Enable caching with 1-hour TTL
card = scrython.cards.Named(fuzzy='Lightning Bolt', cache=True, cache_ttl=3600)

# First call - hits API
card1 = scrython.cards.Named(fuzzy='Lightning Bolt', cache=True)

# Second call - returns cached result (within TTL)
card2 = scrython.cards.Named(fuzzy='Lightning Bolt', cache=True)  # No API call

# Custom TTL
card = scrython.cards.Search(q='bolt', cache=True, cache_ttl=7200)  # 2 hours

# Disable caching (default)
card = scrython.cards.Named(fuzzy='Lightning Bolt')  # cache=False by default
```

### Design Details

**Cache Architecture:**
```python
class CacheBackend(ABC):
    @abstractmethod
    def get(self, key: str) -> dict | None:
        """Retrieve cached data if exists and not expired."""
        pass

    @abstractmethod
    def set(self, key: str, data: dict, ttl: int):
        """Store data with TTL in seconds."""
        pass

    @abstractmethod
    def clear(self):
        """Clear all cached data."""
        pass

class MemoryCache(CacheBackend):
    def __init__(self):
        self._cache: dict[str, tuple[dict, float]] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> dict | None:
        with self._lock:
            if key in self._cache:
                data, expiry = self._cache[key]
                if time.time() < expiry:
                    return data
                del self._cache[key]
        return None

    def set(self, key: str, data: dict, ttl: int):
        with self._lock:
            expiry = time.time() + ttl
            self._cache[key] = (data, expiry)
```

**Cache Key Generation:**
```python
def _generate_cache_key(self) -> str:
    """Generate unique cache key from endpoint and params."""
    endpoint = self._endpoint
    params = sorted(self._params.items())
    key_data = (endpoint, tuple(params))
    return hashlib.sha256(str(key_data).encode()).hexdigest()
```

### Testing

- Test cache hits/misses
- Test TTL expiration (cache entry expires after TTL)
- Test cache key generation (same params = same key)
- Test thread safety
- Test with different endpoint types
- Test cache disabled by default

---

## Phase 5: Iteration Support

**Location:** `scrython/base_mixins.py` (ScryfallListMixin)

### Implementation

1. Add `__iter__()` - Iterate directly over `.data` items
2. Add `__len__()` - Return length of current page data
3. Add `iter_all()` - Generator that auto-paginates through all results (yields cards from all pages)

### Example Usage

```python
results = scrython.cards.Search(q='c:red')

# Direct iteration (Pythonic!)
for card in results:
    print(card.name)

# Length of current page
print(len(results))  # 175 (or however many in first page)

# Auto-pagination through all results
for card in results.iter_all():
    print(card.name)  # Fetches all pages automatically
```

### Design Details

```python
class ScryfallListMixin:
    def __iter__(self):
        """Allow direct iteration over list results."""
        return iter(self.data)

    def __len__(self):
        """Return number of items in current page."""
        return len(self.data)

    def iter_all(self):
        """
        Generator that auto-paginates through all results.
        Yields cards from all pages, fetching next page as needed.
        """
        # Yield current page
        yield from self.data

        # Fetch and yield subsequent pages
        current = self
        while current.has_more:
            # Fetch next page using next_page URI
            current = self.__class__(uri=current.next_page)
            yield from current.data
```

### Testing

- Test `__iter__()` on search results
- Test `__len__()` returns correct count
- Test `iter_all()` fetches all pages
- Test with single page results
- Test with empty results
- Test rate limiting interaction with pagination

---

## Phase 6: Convenience Methods

**Locations:** Various mixin files

### Card Convenience Methods

**Location:** `scrython/cards/cards_mixins.py`

1. `is_legal_in(format: str) -> bool` - Check legality in format
2. `has_color(color: str) -> bool` - Check if card contains color (R, U, B, G, W)
3. `is_creature/is_instant/is_sorcery/is_enchantment/is_artifact/is_planeswalker` - Type checking properties
4. `lowest_price() -> float | None` - Return lowest non-None price across all formats
5. `highest_price() -> float | None` - Return highest price
6. `get_image_url(size: str = 'normal') -> str | None` - Handle nullable image_uris, double-faced cards

### Example Usage

```python
card = scrython.cards.Named(fuzzy='Lightning Bolt')

# Legality check
if card.is_legal_in('commander'):
    print('Legal in Commander!')

# Color check
if card.has_color('R'):
    print('Red card!')

# Type checks
if card.is_instant:
    print('Instant speed!')

# Price helpers
cheapest = card.lowest_price()
most_expensive = card.highest_price()

# Image helpers
url = card.get_image_url(size='large')
```

### List Result Methods

**Location:** `scrython/base_mixins.py`

1. `as_dict(key: str) -> dict` - Convert list to dict keyed by specified attribute
2. `filter(predicate) -> list` - Filter results by predicate function
3. `map(func) -> list` - Transform results with function

### Example Usage

```python
results = scrython.cards.Search(q='bolt')

# Convert to dict keyed by name
by_name = results.as_dict(key='name')
print(by_name['Lightning Bolt'])

# Filter results
cheap_cards = results.filter(lambda c: c.lowest_price() and c.lowest_price() < 1.0)

# Transform results
card_names = results.map(lambda c: c.name)
```

### Testing

- Test each convenience method with various inputs
- Test edge cases (missing data, null values, etc.)
- Test with different card types
- Test list methods with empty results
- Test predicate functions in filter/map

---

## Phase 7: Documentation Updates

### Updates Needed

1. **README.md** - Add sections for:
   - Magic methods examples
   - Serialization examples
   - Caching configuration
   - Rate limiting configuration
   - Iteration examples
   - Convenience methods showcase

2. **Docstrings** - Add comprehensive docstrings to all new methods:
   - Parameter descriptions
   - Return type documentation
   - Usage examples
   - Edge case behavior

3. **IMPLEMENTATION_PLAN.md** - Update with:
   - Mark Phase 8 as complete
   - Document all new features
   - Update library status

4. **Type Hints** - Ensure all new methods have proper type annotations

### Example README Section

```markdown
## Advanced Features

### Caching

Enable built-in caching to reduce API calls and improve performance:

```python
# Enable caching with custom TTL
card = scrython.cards.Named(fuzzy='Lightning Bolt', cache=True, cache_ttl=3600)

# Subsequent calls return cached data (within TTL)
card2 = scrython.cards.Named(fuzzy='Lightning Bolt', cache=True)  # No API call
```

### Rate Limiting

Scrython enforces Scryfall's rate limits (10 calls/second) by default:

```python
# Automatic rate limiting (default)
for name in card_names:
    card = scrython.cards.Named(fuzzy=name)  # Automatically throttled

# Opt-out if needed
card = scrython.cards.Named(fuzzy='Lightning Bolt', rate_limit=False)

# Custom rate limit
card = scrython.cards.Search(q='bolt', rate_limit_per_second=5)
```

### Convenience Methods

Common operations made simple:

```python
card = scrython.cards.Named(fuzzy='Lightning Bolt')

# Check legality
if card.is_legal_in('commander'):
    print('Commander legal!')

# Check colors
if card.has_color('R'):
    print('Red card!')

# Price helpers
print(f'Cheapest price: ${card.lowest_price():.2f}')
```
```

---

## Phase 8: Comprehensive Testing

### Testing Plan

1. **Run Existing Test Suite**
   - Verify all 273+ existing tests still pass
   - Ensure backward compatibility

2. **Add New Tests** (estimated 50-75 new tests):
   - Magic methods: 15-20 tests
   - Serialization: 10-15 tests
   - Rate limiting: 10-12 tests
   - Caching: 15-20 tests
   - Iteration: 8-10 tests
   - Convenience methods: 20-25 tests

3. **Integration Tests**
   - Test caching + rate limiting together
   - Test serialization with cached objects
   - Test iteration with rate limiting
   - Test convenience methods with various card types

4. **Performance Tests**
   - Measure cache hit/miss performance
   - Verify rate limiting timing accuracy
   - Test pagination performance with iter_all()

5. **Edge Case Tests**
   - Empty results
   - Null values
   - Missing fields
   - Network errors
   - Cache expiration
   - Thread safety

### Test Organization

```
tests/
├── test_magic_methods.py      # __repr__, __str__, __eq__, __hash__
├── test_serialization.py      # to_dict, to_json, from_dict
├── test_rate_limiting.py      # RateLimiter class, integration
├── test_caching.py            # Cache backend, TTL, key generation
├── test_iteration.py          # __iter__, __len__, iter_all
└── test_convenience.py        # All convenience methods
```

---

## Implementation Order & Rationale

### Order

1. **Magic methods** → Foundation for better debugging
2. **Serialization** → Needed for caching implementation
3. **Rate limiting** → Important before caching (don't cache rate limit errors)
4. **Caching** → Uses serialization methods
5. **Iteration** → Independent, quick win
6. **Convenience methods** → Independent, can be incremental
7. **Documentation** → After all features complete
8. **Testing** → Continuous throughout, final verification at end

### Rationale

- Magic methods first provide better debugging experience throughout development
- Serialization enables caching (need to store/retrieve objects)
- Rate limiting before caching prevents caching error responses
- Iteration and convenience methods are independent and can be done in parallel
- Documentation after implementation ensures accuracy
- Testing throughout with final comprehensive verification

---

## Estimated Effort

| Phase | Task | Hours |
|-------|------|-------|
| 1 | Magic Methods | 2-3 |
| 2 | Serialization | 2-3 |
| 3 | Rate Limiting | 4-6 |
| 4 | Caching | 6-8 |
| 5 | Iteration Support | 2-3 |
| 6 | Convenience Methods | 4-6 |
| 7 | Documentation | 2-3 |
| 8 | Testing | 3-4 |
| **Total** | | **25-36 hours** |

---

## Design Principles

1. **Backward Compatible** - All existing code continues to work unchanged
2. **Opt-in Where Sensible** - New features use sensible defaults but can be configured
3. **Follow Existing Patterns** - Use established architecture (mixins, base classes)
4. **Type Hints Everywhere** - Maintain excellent type coverage
5. **Comprehensive Testing** - Test all functionality thoroughly
6. **Thread Safe** - All shared state protected with locks
7. **Performance Conscious** - Cache and rate limiter designed for minimal overhead
8. **Future-Proof** - Design allows for extensions (e.g., Redis cache backend)

---

## Success Criteria

- ✅ All 273+ existing tests pass
- ✅ 50+ new tests added and passing
- ✅ Type hints coverage maintained at 100%
- ✅ Backward compatibility verified
- ✅ Documentation updated with examples
- ✅ Performance benchmarks show improvement with caching
- ✅ Rate limiting prevents Scryfall API violations
- ✅ Code review by maintainer (if applicable)

---

## Future Enhancements (Out of Scope)

These features were identified but not prioritized for Phase 8:

1. **Async Support** - async/await API for concurrent requests (major undertaking)
2. **Additional Cache Backends** - Redis, SQLite, file-based caching
3. **Request/Response Hooks** - Middleware for logging, monitoring
4. **Testing Utilities** - Mock Scryfall client for end-user testing
5. **Examples Directory** - Working example scripts
6. **CLI Tool** - Command-line interface for common operations
7. **Retry Logic** - Automatic retry with exponential backoff
8. **Input Validation** - Enhanced validation with better error messages

These can be considered for future phases based on user feedback and demand.
