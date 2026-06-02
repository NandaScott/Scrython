"""Rate limiting for Scryfall API requests.

Scryfall requests a rate limit of 10 requests per second for most endpoints,
but enforces a stricter limit on certain card endpoints.

See: https://scryfall.com/docs/api/rate-limits

This module provides a thread-safe rate limiter with a per-class registry,
allowing different endpoint categories to maintain independent rate limits.
"""

import threading
import time
import warnings
from typing import ClassVar


class RateLimitWarning(UserWarning):
    """
    Warns that the active rate limiter exceeds Scryfall's limit for an endpoint.

    Emitted per-request when an injected limiter is faster than the tier the
    endpoint belongs to. Filter it precisely with
    ``warnings.filterwarnings("ignore", category=scrython.RateLimitWarning)``,
    or escalate it to an error in tests with ``"error"``.
    """


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
    def get_global_limiter(cls, calls_per_second: float | None = None) -> "RateLimiter":
        """
        Get or create the global rate limiter for this class.

        Each RateLimiter class or subclass maintains its own independent
        global instance, keyed by class in a shared registry. This allows
        different endpoint categories to enforce different rate limits.

        Args:
            calls_per_second: Deprecated, ignored. Rate is determined by
                the class default. Passing a value emits a DeprecationWarning.

        Returns:
            The global RateLimiter instance for this class
        """
        if calls_per_second is not None:
            warnings.warn(
                "calls_per_second argument to get_global_limiter() is deprecated "
                "and ignored. Rate is determined by the class default.",
                DeprecationWarning,
                stacklevel=2,
            )
        with cls._global_lock:
            if cls not in cls._global_limiters:
                cls._global_limiters[cls] = cls()
            return cls._global_limiters[cls]

    @classmethod
    def reset_all_limiters(cls) -> None:
        """
        Reset all global rate limiters.

        Clears the entire registry, causing new instances to be created
        on the next call to get_global_limiter(). This is primarily
        useful for testing to ensure a clean state between test runs.
        """
        with cls._global_lock:
            cls._global_limiters.clear()

    @classmethod
    def reset_global_limiter(cls) -> None:
        """Deprecated: use reset_all_limiters() instead."""
        warnings.warn(
            "reset_global_limiter() is deprecated, use reset_all_limiters() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        cls.reset_all_limiters()


class SlowRateLimiter(RateLimiter):
    """
    Rate limiter for Scryfall endpoints with stricter rate limits.

    Scryfall enforces 2 requests per second on certain card endpoints
    (search, named, random, collection). This subclass
    provides that slower default rate.
    """

    def __init__(self, calls_per_second: float = 2.0) -> None:
        super().__init__(calls_per_second)


class NullRateLimiter(RateLimiter):
    """
    No-op limiter for callers who explicitly opt out of throttling.

    ``wait()`` does nothing. The connector treats this as a sanctioned bypass
    and suppresses RateLimitWarning for it. Use at your own risk: exceeding
    Scryfall's published limits can get your client throttled or banned. Inject
    via ``ScryfallConnector(rate_limiter=NullRateLimiter())``.
    """

    def __init__(self) -> None:
        super().__init__(float("inf"))

    def wait(self) -> None:
        return
