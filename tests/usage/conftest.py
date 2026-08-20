"""Pytest configuration and shared fixtures for Scrython usage tests."""

import gzip
import json
from collections import deque
from io import BytesIO
from pathlib import Path
from unittest.mock import Mock, patch
from urllib.parse import urlsplit

import pytest

from scrython.rate_limiter import RateLimiter

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _resource(endpoint: str) -> str:
    """Return the leading path segment that identifies an endpoint's resource."""
    return endpoint.strip("/").split("/", 1)[0]


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

    Requests are routed back to the right payload by matching the registered
    endpoint's resource (its leading path segment) against the resource of the
    URL actually requested. Registering two endpoints under the same resource
    (e.g. "cards/named" and "cards/id/rulings") in one test is ambiguous and
    raises; no current test does this.

    Bulk download: register the CDN payload with the special endpoint key
    "bulk-data/download" (a list of card dicts). The download() HTTP call is
    intercepted by a separate patch on bulk_data_mixins.urlopen, and the list
    is served back as gzip-compressed JSONL to match what the CDN sends.

    Usage:
        def test_something(stub_response, load_fixture):
            stub_response("cards/named", load_fixture("cards_named_black_lotus"))
            card = scrython.cards.Named(exact="Black Lotus")
            assert card.name == "Black Lotus"
    """
    registry: dict[str, deque] = {}
    download_registry: list = []

    class _MockResponse:
        def __init__(self, data: dict | list) -> None:
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

    class _MockDownloadResponse:
        """
        Stands in for the CDN response to download(), which is not plain JSON.

        Scryfall hosts jsonl_download_uri as a .jsonl.gz file, so download()
        feeds the response straight to gzip.GzipFile. That reads in sized
        chunks, which is why this cannot reuse _MockResponse.
        """

        def __init__(self, cards: list) -> None:
            jsonl = "\n".join(json.dumps(card) for card in cards).encode("utf-8")
            self._stream = BytesIO(gzip.compress(jsonl))

        def read(self, size: int = -1) -> bytes:
            return self._stream.read(size)

        def __enter__(self):
            return self

        def __exit__(self, *args) -> None:
            pass

    def _urlopen(request):
        if not registry:
            raise ValueError(
                "stub_response: call stub_response(endpoint, payload) before making requests"
            )

        requested = _resource(urlsplit(request.full_url).path)
        matches = [
            (endpoint, queue)
            for endpoint, queue in registry.items()
            if _resource(endpoint) == requested
        ]

        if len(matches) == 1:
            _, queue = matches[0]
            # Pop from the front when multiple payloads remain (successive pages);
            # keep the last item in place so single-payload tests never exhaust.
            payload = queue.popleft() if len(queue) > 1 else queue[0]
            return _MockResponse(payload)
        if not matches:
            raise ValueError(
                f"stub_response: no registered endpoint matches requested resource "
                f"'{requested}' (registered: {sorted(registry)})"
            )
        raise ValueError(
            f"stub_response: multiple registered endpoints match resource "
            f"'{requested}'; cannot disambiguate (registered: {sorted(registry)})"
        )

    def _urlopen_download(_request):
        if not download_registry:
            raise ValueError(
                "stub_response: register a download payload with "
                "stub_response('bulk-data/download', [...]) before calling download()"
            )
        return _MockDownloadResponse(download_registry[0])

    def _register(endpoint: str, *payloads: dict | list) -> None:
        if not payloads:
            raise ValueError("stub_response: register at least one payload")
        if endpoint == "bulk-data/download":
            download_registry.append(payloads[0])
        else:
            registry[endpoint] = deque(payloads)

    # Patch the limiter's wait() itself so the bypass holds regardless of which
    # _rate_limiter_class an endpoint uses; SlowRateLimiter inherits wait, so one
    # patch covers every tier. (Patching the scrython.base.RateLimiter name does
    # not work: _rate_limiter_class captures the class object at import time.)
    with (
        patch.object(RateLimiter, "wait", lambda *_: None),
        patch("scrython.base.urlopen", side_effect=_urlopen),
        patch("scrython.bulk_data.bulk_data_mixins.urlopen", side_effect=_urlopen_download),
    ):
        yield _register


# Injected payload fixtures: each arms the stub seam for one captured payload so
# a test only has to request the fixture by name and construct via the public
# API. The name mirrors the fixture key (`<module>_<endpoint>__<subject>`); the
# value is the endpoint the payload answers for.
_PAYLOAD_FIXTURES = {
    "cards_named__black_lotus": "cards/named",
    "cards_named__lightning_bolt": "cards/named",
    "cards_named__serra_angel": "cards/named",
    "cards_named__wrath_of_god": "cards/named",
    "cards_named__oblivion_ring": "cards/named",
    "cards_named__jace_beleren": "cards/named",
    "cards_named__ornithopter": "cards/named",
    "cards_named__niv_mizzet_parun": "cards/named",
    "cards_named__prices_mixed": "cards/named",
    "cards_named__prices_partial": "cards/named",
    "cards_named__prices_all_null": "cards/named",
    "cards_named__image_none": "cards/named",
    "cards_by_id__normal": "cards/id",
    "cards_by_id__transform": "cards/id",
    "cards_by_id__modal_dfc": "cards/id",
    "cards_by_id__split": "cards/id",
    "cards_by_id__adventure": "cards/id",
    "cards_by_id__saga": "cards/id",
    "cards_by_id__meld": "cards/id",
    "cards_by_id__flip": "cards/id",
    "cards_by_id__leveler": "cards/id",
    "cards_by_id__class": "cards/id",
    "cards_by_id__token": "cards/id",
    "sets_by_code__lea": "sets/code",
    "bulk_data_by_id__oracle_cards": "bulk-data/id",
    "catalogs_creature_types": "catalog/creature-types",
    "rulings_by_id__rules_lawyer": "cards/id/rulings",
    "symbology_all": "symbology",
    "migrations_by_id__merge": "migrations/id",
    "cards_search__multiset": "cards/search",
}


def _make_payload_fixture(endpoint: str, key: str):
    @pytest.fixture
    def _payload(stub_response, load_fixture):
        stub_response(endpoint, load_fixture(key))

    return _payload


# Register one named pytest fixture per captured payload.
for _key, _endpoint in _PAYLOAD_FIXTURES.items():
    globals()[_key] = _make_payload_fixture(_endpoint, _key)


# Minimal synthetic payload for bulk download tests — not a captured API response.
_SAMPLE_BULK_CARDS: list[dict] = [
    {
        "object": "card",
        "id": "f4fa7d2c-3d02-4a5e-8b4d-2e4e3e7f8c9a",
        "oracle_id": "93c2c107-d8f9-4d79-acfa-c6e1aa0e1f1b",
        "name": "Black Lotus",
    },
]


@pytest.fixture
def bulk_data_by_id__oracle_cards_download(bulk_data_by_id__oracle_cards, stub_response):
    stub_response("bulk-data/download", _SAMPLE_BULK_CARDS)


# Multi-page rulings fixture: two synthetic pages for iter_all() pagination tests.
_RULES_LAWYER_ID = "6c02c575-5685-44f5-8b47-89d888529d1b"

_RULINGS_MULTIPAGE_PAGE_1: dict = {
    "object": "list",
    "has_more": True,
    "next_page": f"https://api.scryfall.com/cards/{_RULES_LAWYER_ID}/rulings?page=2",
    "data": [
        {
            "object": "ruling",
            "oracle_id": "0a3d3d5e-fb77-4940-9ece-7ed62bd6413e",
            "source": "wotc",
            "published_at": "2025-01-24",
            "comment": "Page one ruling.",
        }
    ],
}

_RULINGS_MULTIPAGE_PAGE_2: dict = {
    "object": "list",
    "has_more": False,
    "data": [
        {
            "object": "ruling",
            "oracle_id": "0a3d3d5e-fb77-4940-9ece-7ed62bd6413e",
            "source": "wotc",
            "published_at": "2025-01-24",
            "comment": "Page two ruling.",
        }
    ],
}


@pytest.fixture
def rulings_multipage(stub_response):
    stub_response("cards/id/rulings", _RULINGS_MULTIPAGE_PAGE_1, _RULINGS_MULTIPAGE_PAGE_2)


# Synthetic payload fixtures: unlike the captured fixtures above, these are not
# backed by a committed JSON file. They exist for scenarios a single captured
# payload can't cover — a second, mutated payload for the same resource within
# one test, or a fixed item count that a fixture refresh would otherwise drift.
# They still arm the seam here in conftest.py, not in test bodies (see
# tests/usage/CONVENTIONS.md #4).
@pytest.fixture
def cards_named__black_lotus_factory(stub_response, load_fixture):
    """Arm `cards/named` with the Black Lotus payload, optionally under a different id."""
    payload = load_fixture("cards_named__black_lotus")

    def _arm(id_override: str | None = None) -> None:
        stub_response("cards/named", {**payload, "id": id_override} if id_override else payload)

    return _arm


@pytest.fixture
def rulings_by_id__synthetic_five_items(stub_response):
    """Minimal rulings-list payload with a fixed item count, for the list str() format test."""
    stub_response(
        "cards/id/rulings",
        {"object": "list", "has_more": False, "data": [], "total_cards": 5},
    )


@pytest.fixture
def catalog_creature_types__synthetic_three_items(stub_response):
    """Minimal catalog payload with a fixed item count, for the catalog str() format test."""
    stub_response(
        "catalog/creature-types",
        {
            "object": "catalog",
            "uri": "https://api.scryfall.com/catalog/creature-types",
            "total_values": 3,
            "data": ["Advisor", "Aetherborn", "Alien"],
        },
    )
