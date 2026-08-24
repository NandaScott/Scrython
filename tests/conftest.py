"""Pytest configuration and shared fixtures for Scrython tests."""

import pytest

from scrython.cache import reset_global_cache
from scrython.rate_limiter import RateLimiter


@pytest.fixture(autouse=True)
def reset_globals():
    """
    Reset global state before each test.

    Resets rate limiter and cache to ensure tests don't interfere with each other.
    """
    RateLimiter.reset_all_limiters()
    reset_global_cache()
    yield
    RateLimiter.reset_all_limiters()
    reset_global_cache()
