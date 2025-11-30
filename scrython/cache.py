"""Caching layer for Scryfall API responses.

Provides an abstract cache interface and in-memory cache implementation
with TTL (time-to-live) support for reducing API calls.
"""

import hashlib
import threading
import time
from abc import ABC, abstractmethod
from typing import Any


class CacheBackend(ABC):
    """
    Abstract base class for cache backends.

    Custom cache backends (e.g., Redis, SQLite) can be implemented
    by subclassing this interface.
    """

    @abstractmethod
    def get(self, key: str) -> dict[str, Any] | None:
        """
        Retrieve cached data if it exists and hasn't expired.

        Args:
            key: Cache key to retrieve

        Returns:
            Cached data dictionary if found and valid, None otherwise
        """
        pass

    @abstractmethod
    def set(self, key: str, data: dict[str, Any], ttl: int | float) -> None:
        """
        Store data in cache with a TTL (time-to-live).

        Args:
            key: Cache key to store under
            data: Data dictionary to cache
            ttl: Time-to-live in seconds (int or float)
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear all cached data."""
        pass


class MemoryCache(CacheBackend):
    """
    In-memory cache implementation with TTL support.

    This cache stores data in memory using a dictionary. Each entry
    includes an expiration timestamp. Thread-safe for concurrent access.

    Note: Data is lost when the program exits.
    """

    def __init__(self) -> None:
        """Initialize an empty in-memory cache."""
        self._cache: dict[str, tuple[dict[str, Any], float]] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> dict[str, Any] | None:
        """
        Retrieve cached data if it exists and hasn't expired.

        Automatically removes expired entries during retrieval.

        Args:
            key: Cache key to retrieve

        Returns:
            Cached data dictionary if found and valid, None otherwise
        """
        with self._lock:
            if key in self._cache:
                data, expiry = self._cache[key]
                if time.time() < expiry:
                    return data
                # Remove expired entry
                del self._cache[key]
        return None

    def set(self, key: str, data: dict[str, Any], ttl: int | float) -> None:
        """
        Store data in cache with a TTL.

        Args:
            key: Cache key to store under
            data: Data dictionary to cache
            ttl: Time-to-live in seconds (int or float)
        """
        with self._lock:
            expiry = time.time() + ttl
            self._cache[key] = (data.copy(), expiry)

    def clear(self) -> None:
        """Clear all cached data."""
        with self._lock:
            self._cache.clear()

    def size(self) -> int:
        """
        Get the number of cached entries.

        Returns:
            Number of entries currently in cache
        """
        with self._lock:
            return len(self._cache)


def generate_cache_key(endpoint: str, params: dict[str, Any]) -> str:
    """
    Generate a unique cache key from endpoint and parameters.

    The key is a SHA256 hash of the endpoint and sorted parameters,
    ensuring consistent keys for identical requests.

    Args:
        endpoint: API endpoint path
        params: Query parameters dictionary

    Returns:
        Hex string representing the cache key

    Example:
        key = generate_cache_key('/cards/named', {'fuzzy': 'Lightning Bolt'})
    """
    # Sort params for consistent hashing
    sorted_params = sorted(params.items())
    key_data = (endpoint, tuple(sorted_params))
    key_string = str(key_data)
    return hashlib.sha256(key_string.encode()).hexdigest()


# Global cache instance
_global_cache: MemoryCache | None = None
_cache_lock = threading.Lock()


def get_global_cache() -> MemoryCache:
    """
    Get or create the global cache instance.

    Returns:
        The global MemoryCache instance
    """
    global _global_cache
    with _cache_lock:
        if _global_cache is None:
            _global_cache = MemoryCache()
        return _global_cache


def reset_global_cache() -> None:
    """
    Reset the global cache instance.

    Useful for testing to ensure a clean state between tests.
    """
    global _global_cache
    with _cache_lock:
        if _global_cache is not None:
            _global_cache.clear()
        _global_cache = None
