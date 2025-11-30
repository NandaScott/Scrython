"""Tests for caching functionality."""

import contextlib
import time

from scrython.base import ScrythonRequestHandler
from scrython.cache import MemoryCache, generate_cache_key, get_global_cache, reset_global_cache


class TestMemoryCache:
    """Test the MemoryCache implementation."""

    def test_cache_initialization(self):
        """Test that MemoryCache initializes empty."""
        cache = MemoryCache()
        assert cache.size() == 0

    def test_cache_set_and_get(self):
        """Test basic set and get operations."""
        cache = MemoryCache()
        data = {"name": "Test Card", "id": "123"}

        cache.set("test_key", data, ttl=3600)
        retrieved = cache.get("test_key")

        assert retrieved == data
        assert cache.size() == 1

    def test_cache_get_nonexistent(self):
        """Test getting a key that doesn't exist."""
        cache = MemoryCache()
        result = cache.get("nonexistent")

        assert result is None

    def test_cache_ttl_expiration(self):
        """Test that cache entries expire after TTL."""
        cache = MemoryCache()
        data = {"name": "Test Card"}

        # Set with 0.1 second TTL
        cache.set("test_key", data, ttl=0.1)

        # Should be retrievable immediately
        assert cache.get("test_key") == data

        # Wait for expiration
        time.sleep(0.15)

        # Should be expired
        assert cache.get("test_key") is None
        assert cache.size() == 0  # Expired entry removed

    def test_cache_set_updates_existing(self):
        """Test that setting an existing key updates it."""
        cache = MemoryCache()

        cache.set("key", {"value": 1}, ttl=3600)
        cache.set("key", {"value": 2}, ttl=3600)

        assert cache.get("key") == {"value": 2}
        assert cache.size() == 1  # Still only one entry

    def test_cache_clear(self):
        """Test clearing the cache."""
        cache = MemoryCache()

        cache.set("key1", {"data": 1}, ttl=3600)
        cache.set("key2", {"data": 2}, ttl=3600)
        assert cache.size() == 2

        cache.clear()
        assert cache.size() == 0
        assert cache.get("key1") is None
        assert cache.get("key2") is None

    def test_cache_stores_copy(self):
        """Test that cache stores a copy of data."""
        cache = MemoryCache()
        data = {"name": "Original"}

        cache.set("key", data, ttl=3600)

        # Modify original
        data["name"] = "Modified"

        # Cached data should be unchanged
        retrieved = cache.get("key")
        assert retrieved is not None
        assert retrieved["name"] == "Original"


class TestCacheKeyGeneration:
    """Test cache key generation."""

    def test_generate_cache_key_consistent(self):
        """Test that same inputs produce same key."""
        key1 = generate_cache_key("/cards/named", {"fuzzy": "Lightning Bolt"})
        key2 = generate_cache_key("/cards/named", {"fuzzy": "Lightning Bolt"})

        assert key1 == key2

    def test_generate_cache_key_different_endpoints(self):
        """Test that different endpoints produce different keys."""
        key1 = generate_cache_key("/cards/named", {"fuzzy": "bolt"})
        key2 = generate_cache_key("/cards/search", {"fuzzy": "bolt"})

        assert key1 != key2

    def test_generate_cache_key_different_params(self):
        """Test that different parameters produce different keys."""
        key1 = generate_cache_key("/cards/named", {"fuzzy": "Lightning Bolt"})
        key2 = generate_cache_key("/cards/named", {"fuzzy": "Black Lotus"})

        assert key1 != key2

    def test_generate_cache_key_param_order_independent(self):
        """Test that parameter order doesn't affect key."""
        key1 = generate_cache_key("/cards/search", {"q": "bolt", "order": "name"})
        key2 = generate_cache_key("/cards/search", {"order": "name", "q": "bolt"})

        assert key1 == key2

    def test_generate_cache_key_is_string(self):
        """Test that generated key is a string."""
        key = generate_cache_key("/cards/named", {"fuzzy": "bolt"})

        assert isinstance(key, str)
        assert len(key) == 64  # SHA256 hex digest length


class TestGlobalCache:
    """Test global cache singleton."""

    def test_get_global_cache_creates_singleton(self):
        """Test that get_global_cache returns a singleton."""
        reset_global_cache()

        cache1 = get_global_cache()
        cache2 = get_global_cache()

        assert cache1 is cache2

    def test_reset_global_cache(self):
        """Test that reset clears the global cache."""
        cache1 = get_global_cache()
        cache1.set("key", {"data": "value"}, ttl=3600)

        reset_global_cache()

        cache2 = get_global_cache()
        assert cache2.get("key") is None


class TestRequestHandlerCaching:
    """Test caching integration with ScrythonRequestHandler."""

    def test_cache_disabled_by_default(self, mock_urlopen, sample_card):
        """Test that caching is disabled by default."""
        reset_global_cache()
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        _handler = TestHandler(fuzzy="Lightning Bolt")

        # Cache should be empty
        cache = get_global_cache()
        assert cache.size() == 0

    def test_cache_stores_response(self, mock_urlopen, sample_card):
        """Test that responses are cached when caching is enabled."""
        reset_global_cache()
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        _handler = TestHandler(fuzzy="Lightning Bolt", cache=True)

        # Cache should have one entry
        cache = get_global_cache()
        assert cache.size() == 1

    def test_cache_hit_skips_api_call(self, mock_urlopen, sample_card):
        """Test that cache hits don't make API calls."""
        reset_global_cache()
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        # First call - should hit API
        _handler1 = TestHandler(fuzzy="Lightning Bolt", cache=True)
        assert len(mock_urlopen.calls) == 1

        # Second call - should use cache
        _handler2 = TestHandler(fuzzy="Lightning Bolt", cache=True)
        assert len(mock_urlopen.calls) == 1  # No additional call

        # Data should be the same
        assert _handler1._scryfall_data == _handler2._scryfall_data

    def test_cache_miss_makes_api_call(self, mock_urlopen, sample_card):
        """Test that cache misses make API calls."""
        reset_global_cache()
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        # Different parameters - different cache keys
        _handler1 = TestHandler(fuzzy="Lightning Bolt", cache=True)
        assert len(mock_urlopen.calls) == 1

        _handler2 = TestHandler(fuzzy="Black Lotus", cache=True)
        assert len(mock_urlopen.calls) == 2  # Made another call

    def test_cache_custom_ttl(self, mock_urlopen, sample_card):
        """Test that custom TTL values work."""
        reset_global_cache()
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        # Cache with 0.1 second TTL
        _handler1 = TestHandler(fuzzy="Lightning Bolt", cache=True, cache_ttl=0.1)
        assert len(mock_urlopen.calls) == 1

        # Immediately after - should use cache
        _handler2 = TestHandler(fuzzy="Lightning Bolt", cache=True, cache_ttl=0.1)
        assert len(mock_urlopen.calls) == 1

        # Wait for expiration
        time.sleep(0.15)

        # Should make new API call
        _handler3 = TestHandler(fuzzy="Lightning Bolt", cache=True, cache_ttl=0.1)
        assert len(mock_urlopen.calls) == 2

    def test_cache_different_endpoints_different_keys(self, mock_urlopen, sample_card):
        """Test that different endpoints use different cache keys."""
        reset_global_cache()
        mock_urlopen.set_response(data=sample_card)

        class Handler1(ScrythonRequestHandler):
            _endpoint = "cards/named"

        class Handler2(ScrythonRequestHandler):
            _endpoint = "cards/random"

        _h1 = Handler1(fuzzy="bolt", cache=True)
        _h2 = Handler2(cache=True)

        # Should have made two API calls (different endpoints)
        assert len(mock_urlopen.calls) == 2

        # Should have two cache entries
        cache = get_global_cache()
        assert cache.size() == 2

    def test_cache_doesnt_store_errors(self, mock_urlopen):
        """Test that error responses are not cached."""
        reset_global_cache()
        mock_urlopen.set_error_response(
            {"status": 404, "code": "not_found", "details": "Not found"}
        )

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        with contextlib.suppress(Exception):
            _handler = TestHandler(fuzzy="Nonexistent", cache=True)

        # Cache should be empty (errors not cached)
        cache = get_global_cache()
        assert cache.size() == 0

    def test_cache_with_rate_limiting(self, mock_urlopen, sample_card):
        """Test that caching works alongside rate limiting."""
        reset_global_cache()
        mock_urlopen.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        # First call with both cache and rate limit
        start = time.time()
        _handler1 = TestHandler(fuzzy="bolt", cache=True, rate_limit=True)
        first_call = time.time() - start

        # Second call - should use cache (no rate limit delay)
        start = time.time()
        _handler2 = TestHandler(fuzzy="bolt", cache=True, rate_limit=True)
        second_call = time.time() - start

        # Second call should be much faster (cache hit)
        assert second_call < first_call
        assert second_call < 0.01  # Very fast

    def test_cache_multiple_parameters(self, mock_urlopen):
        """Test caching with multiple query parameters."""
        reset_global_cache()
        list_data = {
            "object": "list",
            "has_more": False,
            "data": [{"id": "1", "name": "Card 1"}],
        }
        mock_urlopen.set_response(data=list_data)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/search"

        # Call with multiple params
        _h1 = TestHandler(q="bolt", order="name", cache=True)
        assert len(mock_urlopen.calls) == 1

        # Same params - should use cache
        _h2 = TestHandler(q="bolt", order="name", cache=True)
        assert len(mock_urlopen.calls) == 1

        # Different order of same params - should still use cache
        _h3 = TestHandler(order="name", q="bolt", cache=True)
        assert len(mock_urlopen.calls) == 1
