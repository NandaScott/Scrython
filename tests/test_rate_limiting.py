"""Tests for rate limiting functionality."""

import contextlib
import time

import pytest

import scrython
from scrython.base import ScryfallError, ScrythonRequestHandler
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


class TestRequestHandlerRateLimiting:
    """Test rate limiting integration with ScrythonRequestHandler."""

    @pytest.fixture
    def mock_urlopen_with_rate_limit(self):
        """Mock urlopen without disabling rate limiting."""
        import http.client
        import io
        import json
        import urllib.error
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
                url = request.get_full_url() if hasattr(request, "get_full_url") else str(request)
                self.calls.append(
                    {
                        "url": url,
                        "method": request.get_method() if hasattr(request, "get_method") else "GET",
                        "headers": dict(request.headers) if hasattr(request, "headers") else {},
                    }
                )

                if self.response_data is None:
                    raise ValueError("No response data set. Call set_response() first.")

                # Real urlopen raises HTTPError for 4xx/5xx status codes
                if self.status >= 400:
                    body = (
                        self.response_data.encode("utf-8")
                        if isinstance(self.response_data, str)
                        else self.response_data
                    )
                    headers = http.client.HTTPMessage()
                    headers["Content-Type"] = "application/json; charset=utf-8"
                    raise urllib.error.HTTPError(
                        url=url,
                        code=self.status,
                        msg=f"HTTP Error {self.status}",
                        hdrs=headers,
                        fp=io.BytesIO(body),
                    )

                return MockURLResponse(self.response_data, self.status)

        mock = MockURLOpen()

        with patch("scrython.connectors.scryfall_api.urlopen", side_effect=mock):
            yield mock

    def test_rate_limit_enabled_by_default(self, mock_urlopen_with_rate_limit, sample_card):
        """Test that rate limiting is enabled by default."""
        # Reset rate limiter
        RateLimiter.reset_all_limiters()

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

    def test_slow_rate_limiter_attributes_via_global(
        self, mock_urlopen_with_rate_limit, sample_card
    ):
        """Test that SlowRateLimiter global instance has correct default attributes."""
        from scrython.rate_limiter import SlowRateLimiter

        # Reset rate limiter
        RateLimiter.reset_all_limiters()

        mock_urlopen_with_rate_limit.set_response(data=sample_card)

        limiter = SlowRateLimiter.get_global_limiter()

        assert limiter.calls_per_second == 2.0
        assert limiter.min_interval == 0.5

    def test_rate_limit_respects_previous_calls(self, mock_urlopen_with_rate_limit, sample_card):
        """Test that rate limiting considers timing of previous calls."""
        # Reset rate limiter
        RateLimiter.reset_all_limiters()

        mock_urlopen_with_rate_limit.set_response(data=sample_card)

        # Fast-tier endpoint (10/s, 0.1s interval) — the slow endpoints
        # (search/named/random/collection) run at 2/s, which this timing math
        # would not match.
        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/multiverse/123"

        # First call
        _handler1 = TestHandler(fuzzy="Card 1")

        # Wait half the interval
        time.sleep(0.05)

        # Second call should still wait a bit
        start = time.time()
        _handler2 = TestHandler(fuzzy="Card 2")
        elapsed = time.time() - start

        # Should wait ~0.05s (remaining time)
        assert 0.03 < elapsed < 0.15

    def test_rate_limit_multiple_handlers_share_limiter(
        self, mock_urlopen_with_rate_limit, sample_card
    ):
        """Test that multiple handlers share the same global rate limiter."""
        # Reset rate limiter
        RateLimiter.reset_all_limiters()

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
        RateLimiter.reset_all_limiters()

        mock_urlopen_with_rate_limit.set_error_response(
            {"status": 404, "code": "not_found", "details": "Not found"}
        )

        class TestHandler(ScrythonRequestHandler):
            _endpoint = "cards/named"

        # Make two calls that will error
        start = time.time()
        with contextlib.suppress(ScryfallError):
            _handler1 = TestHandler(fuzzy="Nonexistent 1")

        with contextlib.suppress(ScryfallError):
            _handler2 = TestHandler(fuzzy="Nonexistent 2")

        elapsed = time.time() - start

        # Should still be rate limited
        assert elapsed > 0.08


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


class TestPerEndpointTiering:
    """ScryfallConnector owns per-endpoint rate-limit tiering (issue #170 review)."""

    def _connector(self, **kwargs):
        from scrython.connectors.scryfall_api import ScryfallConnector

        return ScryfallConnector(**kwargs)

    def test_slow_endpoints_use_slow_tier(self):
        from scrython.rate_limiter import SlowRateLimiter

        conn = self._connector()
        for endpoint in ("cards/search", "cards/named", "cards/random", "cards/collection"):
            assert isinstance(conn._limiter_for(endpoint), SlowRateLimiter)

    def test_fast_endpoints_use_default_tier(self):
        from scrython.rate_limiter import RateLimiter, SlowRateLimiter

        limiter = self._connector()._limiter_for("cards/some-id")
        assert isinstance(limiter, RateLimiter)
        assert not isinstance(limiter, SlowRateLimiter)

    def test_injected_limiter_overrides_tiering(self):
        import warnings

        from scrython.rate_limiter import RateLimitWarning

        fixed = RateLimiter(20.0)
        conn = self._connector(rate_limiter=fixed)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RateLimitWarning)
            assert conn._limiter_for("cards/search") is fixed
            assert conn._limiter_for("cards/some-id") is fixed

    def test_over_limit_injection_warns(self):
        from scrython.rate_limiter import RateLimiter, RateLimitWarning

        conn = self._connector(rate_limiter=RateLimiter(10.0))  # 10/s > slow 2/s limit
        with pytest.warns(RateLimitWarning):
            conn._limiter_for("cards/search")

    def test_within_limit_injection_is_silent(self, recwarn):
        from scrython.rate_limiter import RateLimiter, RateLimitWarning

        self._connector(rate_limiter=RateLimiter(2.0))._limiter_for("cards/search")
        assert not [w for w in recwarn.list if issubclass(w.category, RateLimitWarning)]

    def test_default_tiered_path_is_silent(self, recwarn):
        from scrython.rate_limiter import RateLimitWarning

        conn = self._connector()
        conn._limiter_for("cards/search")
        conn._limiter_for("cards/some-id")
        assert not [w for w in recwarn.list if issubclass(w.category, RateLimitWarning)]

    def test_null_rate_limiter_suppresses_warning(self, recwarn):
        from scrython.rate_limiter import NullRateLimiter, RateLimitWarning

        self._connector(rate_limiter=NullRateLimiter())._limiter_for("cards/search")
        assert not [w for w in recwarn.list if issubclass(w.category, RateLimitWarning)]

    def test_null_rate_limiter_wait_is_noop(self):
        from scrython.rate_limiter import NullRateLimiter

        limiter = NullRateLimiter()
        start = time.time()
        for _ in range(5):
            limiter.wait()
        assert time.time() - start < 0.05

    def test_slow_endpoint_set_matches_card_endpoints(self):
        """Drift guard: every slow endpoint string maps to a real cards.py endpoint."""
        from scrython.cards import cards as cards_module
        from scrython.connectors.scryfall_api import ScryfallConnector

        defined: set[str] = set()
        for name in dir(cards_module):
            obj = getattr(cards_module, name)
            if isinstance(obj, type) and issubclass(obj, ScrythonRequestHandler):
                endpoint = getattr(obj, "_endpoint", "")
                if endpoint:
                    defined.add(endpoint.strip("/"))

        assert defined >= ScryfallConnector._SLOW_ENDPOINTS


class TestRemovedRateLimitKwarg:
    """The per-request rate_limit= toggle is removed (issue #170 review)."""

    def test_rate_limit_kwarg_warns_deprecation(self, mock_urlopen, sample_card):
        mock_urlopen.set_response(data=sample_card)
        with pytest.warns(DeprecationWarning):
            scrython.cards.ById(id="abc", rate_limit=False)

    def test_rate_limit_kwarg_not_sent_as_query_param(self, mock_urlopen, sample_card):
        mock_urlopen.set_response(data=sample_card)
        with pytest.warns(DeprecationWarning):
            scrython.cards.ById(id="abc", rate_limit=False)
        assert "rate_limit" not in mock_urlopen.calls[0]["url"]
