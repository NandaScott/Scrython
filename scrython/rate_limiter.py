"""Rate limiting for Scryfall API requests.

Scryfall requests a rate limit of 10 requests per second. This module
provides a thread-safe rate limiter that enforces this limit by default,
while allowing users to opt-out or customize the rate limit.
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

    # Class-level (global) rate limiter shared across all instances
    _global_limiter: ClassVar["RateLimiter | None"] = None
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
    def get_global_limiter(cls, calls_per_second: float = 10.0) -> "RateLimiter":
        """
        Get or create the global rate limiter instance.

        This ensures that all API requests share a single rate limiter,
        preventing rate limit violations even when multiple objects are
        created concurrently.

        Args:
            calls_per_second: Rate limit to use if creating a new limiter

        Returns:
            The global RateLimiter instance
        """
        with cls._global_lock:
            if cls._global_limiter is None:
                cls._global_limiter = cls(calls_per_second)
            return cls._global_limiter

    @classmethod
    def reset_global_limiter(cls) -> None:
        """
        Reset the global rate limiter.

        This is primarily useful for testing to ensure a clean state
        between test runs.
        """
        with cls._global_lock:
            cls._global_limiter = None
