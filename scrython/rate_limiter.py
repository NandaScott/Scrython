"""Rate limiting for Scryfall API requests.

Scryfall requests a rate limit of 10 requests per second for most endpoints,
but enforces a stricter 2 requests per second for certain card endpoints.

This module provides a thread-safe rate limiter with a per-class registry,
allowing different endpoint categories to maintain independent rate limits.
"""

import threading
import time
from typing import ClassVar


class RateLimiter:
    """
    Thread-safe rate limiter using token bucket algorithm.

    This limiter enforces a maximum number of calls per second by tracking
    the time between calls and sleeping if necessary to maintain the rate limit.

    The limiter is thread-safe and can be shared across multiple threads.
    """

    # Per-class registry of global rate limiter instances
    _global_limiters: ClassVar[dict[type, "RateLimiter"]] = {}
    _global_lock: ClassVar[threading.Lock] = threading.Lock()

    def __init__(self, calls_per_second: float = 10.0) -> None:
        """
        Initialize a rate limiter.

        Args:
            calls_per_second: Maximum number of calls allowed per second.
                             Default is 10.0 per Scryfall guidelines.
        """
        self.calls_per_second = calls_per_second
        self.min_interval = 1.0 / calls_per_second
        self.last_call = 0.0
        self.lock = threading.Lock()

    def wait(self) -> None:
        """
        Block until the rate limit allows the next call.

        This method is thread-safe and will sleep if necessary to maintain
        the configured rate limit. Multiple threads calling this method will
        be properly synchronized.

        Example:
            limiter = RateLimiter(calls_per_second=10)
            limiter.wait()  # May sleep to enforce rate limit
            make_api_call()
        """
        with self.lock:
            now = time.time()
            time_since_last = now - self.last_call

            if time_since_last < self.min_interval:
                sleep_time = self.min_interval - time_since_last
                time.sleep(sleep_time)

            self.last_call = time.time()

    @classmethod
    def get_global_limiter(cls) -> "RateLimiter":
        """
        Get or create the global rate limiter for this class.

        Each RateLimiter subclass maintains its own independent global
        instance, keyed by class in a shared registry. This allows
        different endpoint categories to enforce different rate limits.

        Returns:
            The global RateLimiter instance for this class
        """
        with cls._global_lock:
            if cls not in cls._global_limiters:
                cls._global_limiters[cls] = cls()
            return cls._global_limiters[cls]

    @classmethod
    def reset_global_limiter(cls) -> None:
        """
        Reset all global rate limiters.

        Clears the entire registry, causing new instances to be created
        on the next call to get_global_limiter(). This is primarily
        useful for testing to ensure a clean state between test runs.
        """
        with cls._global_lock:
            cls._global_limiters.clear()


class SlowRateLimiter(RateLimiter):
    """
    Rate limiter for Scryfall endpoints with stricter rate limits.

    Scryfall enforces 2 requests per second on certain card endpoints
    (search, named, random, collection). This subclass
    provides that slower default rate.
    """

    def __init__(self, calls_per_second: float = 2.0) -> None:
        super().__init__(calls_per_second)
