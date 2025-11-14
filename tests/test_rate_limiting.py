"""Tests for rate limiting functionality."""

import contextlib
import time

import pytest

from scrython.base import ScrythonRequestHandler
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

        # Should be very fast (< 0.01s)
        assert first_call_time < 0.01

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
        assert elapsed < 0.01

    def test_rate_limiter_multiple_calls(self):
        """Test RateLimiter with multiple sequential calls."""
        limiter = RateLimiter(calls_per_second=20.0)  # 0.05s interval

        start = time.time()
        for _ in range(5):
            limiter.wait()
        elapsed = time.time() - start

        # Should take ~0.2s (4 intervals * 0.05s)
        # First call is immediate, then 4 waits of 0.05s each
        assert 0.15 < elapsed < 0.3

    def test_get_global_limiter_creates_singleton(self):
        """Test that get_global_limiter returns a singleton."""
        # Reset first
        RateLimiter.reset_global_limiter()

        limiter1 = RateLimiter.get_global_limiter()
        limiter2 = RateLimiter.get_global_limiter()

        # Should be the same instance
        assert limiter1 is limiter2

    def test_reset_global_limiter(self):
        """Test that reset_global_limiter clears the singleton."""
        # Create a global limiter
        limiter1 = RateLimiter.get_global_limiter()

        # Reset
        RateLimiter.reset_global_limiter()

        # Get another - should be a new instance
        limiter2 = RateLimiter.get_global_limiter()

        assert limiter1 is not limiter2


class TestRequestHandlerRateLimiting:
    """Test rate limiting integration with ScrythonRequestHandler."""

    @pytest.fixture
    def mock_urlopen_with_rate_limit(self):
        """Mock urlopen without disabling rate limiting."""
        import json
        from unittest.mock import Mock, patch

        class MockURLResponse:
            def __init__(self, data, status=200):
                self.data = data.encode("utf-8") if isinstance(data, str) else data
                self.status = status
                self._info = Mock()
                self._info.get_param = Mock(return_value="utf-8")

            def read(self):
                return self.data

            def info(self):
                return self._info

            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

        class MockURLOpen:
            def __init__(self):
                self.response_data = None
                self.calls = []

            def set_response(self, data=None, status=200):
                """Set the mock response data."""
                if data:
                    self.response_data = json.dumps(data) if isinstance(data, dict) else data
                else:
                    raise ValueError("Must provide data")
                self.status = status

            def set_error_response(self, error_data):
                """Set a Scryfall error response."""
                error = {
                    "object": "error",
                    "status": error_data.get("status", 404),
                    "code": error_data.get("code", "not_found"),
                    "details": error_data.get("details", "Not found"),
                    "type": error_data.get("type", None),
                    "warnings": error_data.get("warnings", None),
                }
                self.response_data = json.dumps(error)
                self.status = error_data.get("status", 404)

            def __call__(self, request):
                self.calls.append(
                    {
                        "url": (
                            request.get_full_url()
                            if hasattr(request, "get_full_url")
                            else str(request)
                        ),
                        "method": request.get_method() if hasattr(request, "get_method") else "GET",
                        "headers": dict(request.headers) if hasattr(request, "headers") else {},
                    }
                )

                if self.response_data is None:
                    raise ValueError("No response data set. Call set_response() first.")

                return MockURLResponse(self.response_data, self.status)

        mock = MockURLOpen()

        with patch("scrython.base.urlopen", side_effect=mock):
            yield mock

    def test_rate_limit_enabled_by_default(self, mock_urlopen_with_rate_limit, sample_card):
        """Test that rate limiting is enabled by default."""
        # Reset rate limiter
        RateLimiter.reset_global_limiter()

        mock_urlopen_with_rate_limit.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        # Make two calls quickly
        start = time.time()
        _handler1 = TestHandler(fuzzy="Card 1")
        _handler2 = TestHandler(fuzzy="Card 2")
        elapsed = time.time() - start

        # Second call should have been rate limited (~0.1s delay)
        assert elapsed > 0.08

    def test_rate_limit_can_be_disabled(self, mock_urlopen_with_rate_limit, sample_card):
        """Test that rate limiting can be disabled."""
        # Reset rate limiter
        RateLimiter.reset_global_limiter()

        mock_urlopen_with_rate_limit.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        # Make two calls quickly with rate limiting disabled
        start = time.time()
        _handler1 = TestHandler(fuzzy="Card 1", rate_limit=False)
        _handler2 = TestHandler(fuzzy="Card 2", rate_limit=False)
        elapsed = time.time() - start

        # Should be very fast (no rate limiting)
        assert elapsed < 0.05

    def test_custom_rate_limit(self, mock_urlopen_with_rate_limit, sample_card):
        """Test that custom rate limits can be specified."""
        # Reset rate limiter
        RateLimiter.reset_global_limiter()

        mock_urlopen_with_rate_limit.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        # Use a slower rate limit (5 calls/sec = 0.2s interval)
        start = time.time()
        _handler1 = TestHandler(fuzzy="Card 1", rate_limit_per_second=5.0)
        _handler2 = TestHandler(fuzzy="Card 2", rate_limit_per_second=5.0)
        elapsed = time.time() - start

        # Should wait ~0.2s
        assert elapsed > 0.18

    def test_rate_limit_respects_previous_calls(self, mock_urlopen_with_rate_limit, sample_card):
        """Test that rate limiting considers timing of previous calls."""
        # Reset rate limiter
        RateLimiter.reset_global_limiter()

        mock_urlopen_with_rate_limit.set_response(data=sample_card)

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        # First call
        _handler1 = TestHandler(fuzzy="Card 1")

        # Wait half the interval
        time.sleep(0.05)

        # Second call should still wait a bit
        start = time.time()
        _handler2 = TestHandler(fuzzy="Card 2")
        elapsed = time.time() - start

        # Should wait ~0.05s (remaining time)
        assert 0.03 < elapsed < 0.08

    def test_rate_limit_multiple_handlers_share_limiter(
        self, mock_urlopen_with_rate_limit, sample_card
    ):
        """Test that multiple handlers share the same global rate limiter."""
        # Reset rate limiter
        RateLimiter.reset_global_limiter()

        mock_urlopen_with_rate_limit.set_response(data=sample_card)

        class HandlerA(ScrythonRequestHandler):
            _endpoint = "cards/named"

        class HandlerB(ScrythonRequestHandler):
            _endpoint = "cards/random"

        # Make calls to different handlers
        start = time.time()
        _handler1 = HandlerA(fuzzy="Card 1")
        _handler2 = HandlerB()
        elapsed = time.time() - start

        # Should be rate limited even though different handler classes
        assert elapsed > 0.08

    def test_rate_limit_with_errors_still_enforced(self, mock_urlopen_with_rate_limit):
        """Test that rate limiting is enforced even when API returns errors."""
        # Reset rate limiter
        RateLimiter.reset_global_limiter()

        mock_urlopen_with_rate_limit.set_error_response(
            {"status": 404, "code": "not_found", "details": "Not found"}
        )

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        # Make two calls that will error
        start = time.time()
        with contextlib.suppress(Exception):
            _handler1 = TestHandler(fuzzy="Nonexistent 1")

        with contextlib.suppress(Exception):
            _handler2 = TestHandler(fuzzy="Nonexistent 2")

        elapsed = time.time() - start

        # Should still be rate limited
        assert elapsed > 0.08
