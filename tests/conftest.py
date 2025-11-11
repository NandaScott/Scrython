"""Pytest configuration and shared fixtures for Scrython tests."""

import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Path to fixture files
FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixtures_dir():
    """Return the path to the fixtures directory."""
    return FIXTURES_DIR


def load_fixture(fixture_path):
    """
    Load a JSON fixture file.

    Args:
        fixture_path: Path to the fixture file relative to tests/fixtures/

    Returns:
        Parsed JSON data from the fixture file
    """
    full_path = FIXTURES_DIR / fixture_path
    with open(full_path) as f:
        return json.load(f)


@pytest.fixture
def mock_urlopen():
    """
    Fixture that mocks urllib.request.urlopen for testing HTTP requests.

    Usage in tests:
        def test_something(mock_urlopen):
            mock_urlopen.set_response('cards/named.json')
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

        def set_response(self, fixture_path=None, data=None, status=200):
            """
            Set the mock response data.

            Args:
                fixture_path: Path to a JSON fixture file (e.g., 'cards/named.json')
                data: Direct data to return (dict or string)
                status: HTTP status code (default: 200)
            """
            if fixture_path:
                self.response_data = json.dumps(load_fixture(fixture_path))
            elif data:
                self.response_data = json.dumps(data) if isinstance(data, dict) else data
            else:
                raise ValueError("Must provide either fixture_path or data")

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
            self.calls.append(
                {
                    "url": (
                        request.get_full_url() if hasattr(request, "get_full_url") else str(request)
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


@pytest.fixture
def sample_set():
    """Sample set data for testing."""
    return {
        "object": "set",
        "id": "1d4e-28d6-4726-b9fd-3f52-f5fdca",
        "code": "lea",
        "name": "Limited Edition Alpha",
        "uri": "https://api.scryfall.com/sets/1d4e-28d6-4726-b9fd-3f52-f5fdca",
        "released_at": "1993-08-05",
        "set_type": "core",
        "card_count": 295,
    }


@pytest.fixture
def sample_bulk_data():
    """Sample bulk data object for testing."""
    return {
        "object": "bulk_data",
        "id": "27bf3214-1271-490b-bdfe-c0be6c23d02e",
        "type": "oracle_cards",
        "name": "Oracle Cards",
        "description": "All cards, each uniquely identified by Oracle ID",
        "download_uri": "https://api.scryfall.com/bulk-data/27bf3214-1271-490b-bdfe-c0be6c23d02e/download",
        "updated_at": "2025-01-01T12:00:00.000Z",
        "size": 123456789,
    }


@pytest.fixture
def sample_list_response():
    """Sample list response structure."""
    return {"object": "list", "has_more": False, "data": []}


@pytest.fixture
def sample_catalog_response():
    """Sample catalog response structure."""
    return {"object": "catalog", "total_values": 0, "data": []}
