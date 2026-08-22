"""Pytest configuration and shared fixtures for Scrython tests."""

import http.client
import io
import json
import urllib.error
from unittest.mock import Mock, patch

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


@pytest.fixture
def disable_rate_limiting():
    """
    Fixture that disables rate limiting for tests.

    This makes tests run much faster by removing rate limit delays.
    """
    with patch("scrython.base.RateLimiter") as mock_limiter_class:
        mock_instance = Mock()
        mock_instance.wait = Mock()  # No-op wait method
        mock_limiter_class.get_global_limiter.return_value = mock_instance
        yield


@pytest.fixture
def mock_urlopen(disable_rate_limiting):  # noqa: ARG001
    """
    Fixture that mocks urllib.request.urlopen for testing HTTP requests.

    Automatically disables rate limiting to keep tests fast.

    Usage in tests:
        def test_something(mock_urlopen):
            mock_urlopen.set_response(data={"object": "card", "name": "Black Lotus"})
            card = scrython.Cards(fuzzy='Black Lotus')
            assert card.name == 'Black Lotus'
    """

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
            """
            Set the mock response data.

            Args:
                data: Direct data to return (dict or string)
                status: HTTP status code (default: 200)
            """
            if not data:
                raise ValueError("Must provide data")

            self.response_data = json.dumps(data) if isinstance(data, dict) else data
            self.status = status

        def set_error_response(self, error_data):
            """
            Set a Scryfall error response.

            Args:
                error_data: Dictionary containing error fields
            """
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
            # Record the call for assertion purposes
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

    with patch("scrython.base.urlopen", side_effect=mock):
        yield mock


@pytest.fixture
def sample_card():
    """Sample card data for testing."""
    return {
        "object": "card",
        "id": "f4fa7d2c-3d02-4a5e-8b4d-2e4e3e7f8c9a",
        "name": "Black Lotus",
        "mana_cost": "{0}",
        "cmc": 0.0,
        "type_line": "Artifact",
        "oracle_text": "{T}, Sacrifice Black Lotus: Add three mana of any one color.",
        "colors": [],
        "color_identity": [],
        "set": "lea",
        "set_name": "Limited Edition Alpha",
        "rarity": "rare",
        "artist": "Christopher Rush",
        "prices": {"usd": "25000.00", "usd_foil": None, "eur": None, "tix": None},
    }
