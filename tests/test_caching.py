"""Tests for caching functionality."""

import time

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
