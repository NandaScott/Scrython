"""Pytest configuration and shared fixtures for Scrython usage tests."""

import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def load_fixture():
    """Return a loader that reads a committed JSON fixture by key."""

    def _load(key: str) -> dict:
        full_path = FIXTURES_DIR / f"{key}.json"
        with open(full_path) as f:
            data = json.load(f)

        provenance = data.get("_provenance")
        if not isinstance(provenance, dict):
            raise ValueError(
                f"Fixture '{key}' is missing a '_provenance' header. "
                "Re-run scripts/capture_fixtures.py to refresh it."
            )
        required_fields = {"captured_at", "endpoint", "source_url"}
        missing = required_fields - provenance.keys()
        if missing:
            raise ValueError(
                f"Fixture '{key}' provenance is missing required fields: {sorted(missing)}."
            )

        payload = data.get("payload")
        if not isinstance(payload, dict):
            raise ValueError(
                f"Fixture '{key}' is missing a 'payload' field. "
                "Re-run scripts/capture_fixtures.py to refresh it."
            )
        return payload

    return _load


@pytest.fixture
def stub_response():
    """
    Seam fixture: register a payload for an endpoint and stub the HTTP call.

    This is the only place in the usage suite that references the mock seam
    (urlopen patch + rate-limiter bypass). Post-#169: swap this body to
    MockConnector + use_connector() with no test-body changes required.

    Usage:
        def test_something(stub_response, load_fixture):
            stub_response("cards/named", load_fixture("cards_named_black_lotus"))
            card = scrython.cards.Named(exact="Black Lotus")
            assert card.name == "Black Lotus"
    """
    registry: dict = {}

    class _MockResponse:
        def __init__(self, data: dict) -> None:
            self._data = json.dumps(data).encode("utf-8")
            self._info = Mock()
            self._info.get_param = Mock(return_value="utf-8")

        def read(self) -> bytes:
            return self._data

        def info(self):
            return self._info

        def __enter__(self):
            return self

        def __exit__(self, *args) -> None:
            pass

    def _urlopen(request):  # noqa: ARG001
        if not registry:
            raise ValueError(
                "stub_response: call stub_response(endpoint, payload) before making requests"
            )
        payload = next(iter(registry.values()))
        return _MockResponse(payload)

    def _register(endpoint: str, payload: dict) -> None:
        registry[endpoint] = payload

    with patch("scrython.base.RateLimiter") as mock_limiter_class:
        mock_instance = Mock()
        mock_instance.wait = Mock()
        mock_limiter_class.get_global_limiter.return_value = mock_instance
        with patch("scrython.base.urlopen", side_effect=_urlopen):
            yield _register
