"""Tests for rate limiting functionality."""

import time

import pytest

from scrython.rate_limiter import RateLimiter


class TestRateLimiter:
    """Test the RateLimiter class."""

    def test_rate_limiter_initialization(self):
        """Test that RateLimiter initializes with correct settings."""
        limiter = RateLimiter(calls_per_second=10.0)

        assert limiter.calls_per_second == 10.0
        assert limiter.min_interval == 0.1  # 1/10

    def test_rate_limiter_custom_rate(self):
        """Test RateLimiter with custom rate."""
        limiter = RateLimiter(calls_per_second=5.0)

        assert limiter.calls_per_second == 5.0
        assert limiter.min_interval == 0.2  # 1/5

    def test_rate_limiter_enforces_delay(self):
        """Test that RateLimiter enforces delays between calls."""
        limiter = RateLimiter(calls_per_second=10.0)

        # First call should not wait
        start = time.time()
        limiter.wait()
        first_call_time = time.time() - start

        # Should be very fast
        assert first_call_time < 0.05

        # Second call immediately after should wait
        start = time.time()
        limiter.wait()
        second_call_time = time.time() - start

        # Should wait ~0.1s (with some tolerance for system variance)
        assert 0.08 < second_call_time < 0.15

    def test_rate_limiter_no_delay_after_interval(self):
        """Test that RateLimiter doesn't delay if enough time has passed."""
        limiter = RateLimiter(calls_per_second=10.0)

        # First call
        limiter.wait()

        # Wait longer than the interval
        time.sleep(0.15)

        # Second call should not wait
        start = time.time()
        limiter.wait()
        elapsed = time.time() - start

        # Should be very fast
        assert elapsed < 0.05

    def test_rate_limiter_multiple_calls(self):
        """Test RateLimiter with multiple sequential calls."""
        limiter = RateLimiter(calls_per_second=20.0)  # 0.05s interval

        start = time.time()
        for _ in range(5):
            limiter.wait()
        elapsed = time.time() - start

        # Should take ~0.2s (4 intervals * 0.05s)
        # First call is immediate, then 4 waits of 0.05s each
        assert 0.15 < elapsed < 0.5

    def test_get_global_limiter_creates_singleton(self):
        """Test that get_global_limiter returns a singleton."""
        # Reset first
        RateLimiter.reset_all_limiters()

        limiter1 = RateLimiter.get_global_limiter()
        limiter2 = RateLimiter.get_global_limiter()

        # Should be the same instance
        assert limiter1 is limiter2

    def test_reset_all_limiters(self):
        """Test that reset_all_limiters clears the singleton."""
        # Create a global limiter
        limiter1 = RateLimiter.get_global_limiter()

        # Reset
        RateLimiter.reset_all_limiters()

        # Get another - should be a new instance
        limiter2 = RateLimiter.get_global_limiter()

        assert limiter1 is not limiter2

    def test_global_limiter_registry_per_class(self):
        """Test that different RateLimiter subclasses get independent global instances."""
        from scrython.rate_limiter import SlowRateLimiter

        limiter_fast = RateLimiter.get_global_limiter()
        limiter_slow = SlowRateLimiter.get_global_limiter()

        assert limiter_fast is not limiter_slow
        assert limiter_fast.calls_per_second == 10.0
        assert limiter_slow.calls_per_second == 2.0

    def test_reset_all_limiters_clears_all(self):
        """Test that reset clears the entire registry."""
        from scrython.rate_limiter import SlowRateLimiter

        old_fast = RateLimiter.get_global_limiter()
        old_slow = SlowRateLimiter.get_global_limiter()

        RateLimiter.reset_all_limiters()

        new_fast = RateLimiter.get_global_limiter()
        new_slow = SlowRateLimiter.get_global_limiter()

        assert new_fast is not old_fast
        assert new_slow is not old_slow

    def test_get_global_limiter_deprecated_param(self):
        """Test that passing calls_per_second to get_global_limiter emits a deprecation warning."""
        RateLimiter.reset_all_limiters()

        with pytest.warns(DeprecationWarning, match="calls_per_second.*deprecated"):
            limiter = RateLimiter.get_global_limiter(5.0)

        # Should still return the default limiter (argument is ignored)
        assert limiter.calls_per_second == 10.0


class TestSlowRateLimiter:
    """Test the SlowRateLimiter class."""

    def test_slow_rate_limiter_default_rate(self):
        """Test that SlowRateLimiter defaults to 2 calls per second."""
        from scrython.rate_limiter import SlowRateLimiter

        limiter = SlowRateLimiter()

        assert limiter.calls_per_second == 2.0
        assert limiter.min_interval == 0.5

    def test_slow_rate_limiter_enforces_delay(self):
        """Test that SlowRateLimiter enforces 500ms delays between calls."""
        from scrython.rate_limiter import SlowRateLimiter

        limiter = SlowRateLimiter()

        limiter.wait()

        start = time.time()
        limiter.wait()
        elapsed = time.time() - start

        assert 0.45 < elapsed < 1.0


class TestEndpointRateLimiterAssignment:
    """Test that endpoint classes declare the correct rate limiter class."""

    def test_search_uses_slow_limiter(self):
        from scrython.cards.cards import Search
        from scrython.rate_limiter import SlowRateLimiter

        assert Search._rate_limiter_class is SlowRateLimiter

    def test_named_uses_slow_limiter(self):
        from scrython.cards.cards import Named
        from scrython.rate_limiter import SlowRateLimiter

        assert Named._rate_limiter_class is SlowRateLimiter

    def test_random_uses_slow_limiter(self):
        from scrython.cards.cards import Random
        from scrython.rate_limiter import SlowRateLimiter

        assert Random._rate_limiter_class is SlowRateLimiter

    def test_collection_uses_slow_limiter(self):
        from scrython.cards.cards import Collection
        from scrython.rate_limiter import SlowRateLimiter

        assert Collection._rate_limiter_class is SlowRateLimiter

    def test_autocomplete_uses_default_limiter(self):
        from scrython.cards.cards import Autocomplete
        from scrython.rate_limiter import RateLimiter

        assert Autocomplete._rate_limiter_class is RateLimiter

    def test_by_code_number_uses_default_limiter(self):
        from scrython.cards.cards import ByCodeNumber
        from scrython.rate_limiter import RateLimiter

        assert ByCodeNumber._rate_limiter_class is RateLimiter
