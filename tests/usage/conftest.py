"""Pytest configuration and shared fixtures for Scrython usage tests."""

import gzip
import json
from collections import deque
from email.message import Message
from io import BytesIO
from pathlib import Path
from unittest.mock import Mock, patch
from urllib.error import HTTPError
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


class _MockResponse:
    """Stands in for a plain JSON API response."""

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


class _Stub:
    """
    The mock seam: what a request gets back, and through which transport.

    Three ways to arm it, one per transport the library uses. `__call__`
    registers a JSON payload for an endpoint, `download` registers the
    gzipped JSONL a bulk download reads, and `error` arms the HTTP failure
    Scryfall answers a bad request with.
    """

    def __init__(self) -> None:
        self.registry: dict[str, deque] = {}
        self.download_payload: list | None = None
        self.failure: HTTPError | None = None

    def __call__(self, endpoint: str, *payloads: dict) -> None:
        """Register one payload per successive request to `endpoint`."""
        if not payloads:
            raise ValueError("stub_response: register at least one payload")
        self.registry[endpoint] = deque(payloads)

    def download(self, cards: list) -> None:
        """Register the card list a bulk download serves back as gzipped JSONL."""
        self.download_payload = cards

    def error(self, status: int, body: dict) -> None:
        """Arm a Scryfall JSON error body, delivered the way urllib delivers one."""
        headers = Message()
        headers["Content-Type"] = "application/json; charset=utf-8"
        self.failure = HTTPError(
            "https://api.scryfall.com/",
            status,
            body.get("details", ""),
            headers,  # type: ignore[arg-type]
            BytesIO(json.dumps(body).encode("utf-8")),
        )

    def open(self, request) -> _MockResponse:
        """Answer a request on the JSON transport, or fail it if an error is armed."""
        if self.failure is not None:
            raise self.failure
        if not self.registry:
            raise ValueError(
                "stub_response: call stub_response(endpoint, payload) before making requests"
            )

        requested_path = urlsplit(request.full_url).path.strip("/")
        # An endpoint registered under its full path answers only that path.
        # Endpoints whose real URL carries an id (e.g. "cards/id" standing in
        # for "cards/<uuid>") have no exact match, so they fall back to the
        # resource segment as before.
        matches = [
            (endpoint, queue)
            for endpoint, queue in self.registry.items()
            if endpoint.strip("/") == requested_path
        ] or [
            (endpoint, queue)
            for endpoint, queue in self.registry.items()
            if _resource(endpoint) == _resource(requested_path)
        ]

        if len(matches) == 1:
            _, queue = matches[0]
            # Pop from the front when multiple payloads remain (successive pages);
            # keep the last item in place so single-payload tests never exhaust.
            return _MockResponse(queue.popleft() if len(queue) > 1 else queue[0])
        if not matches:
            raise ValueError(
                f"stub_response: no registered endpoint matches requested path "
                f"'{requested_path}' (registered: {sorted(self.registry)})"
            )
        raise ValueError(
            f"stub_response: multiple registered endpoints match resource "
            f"'{_resource(requested_path)}'; cannot disambiguate "
            f"(registered: {sorted(self.registry)})"
        )

    def open_download(self, _request) -> _MockDownloadResponse:
        """Answer a request on the bulk-download transport."""
        if self.download_payload is None:
            raise ValueError(
                "stub_response: register a download payload with "
                "stub_response.download([...]) before calling download()"
            )
        return _MockDownloadResponse(self.download_payload)


@pytest.fixture
def stub_response():
    """
    Seam fixture: register a payload for an endpoint and stub the HTTP call.

    This is the only place in the usage suite that references the mock seam
    (urlopen patch + rate-limiter bypass). Post-#169: swap this body to
    MockConnector + use_connector() with no test-body changes required.

    Requests are routed back to the right payload by matching the registered
    endpoint against the URL actually requested: first on the full path, then
    on the resource (leading path segment) for endpoints registered without
    their id, such as "cards/id". Two endpoints sharing a resource can both be
    registered as long as each is reached by its exact path; registrations that
    only the resource fallback can reach (e.g. "cards/named" and
    "cards/id/rulings") are ambiguous and raise.

    See _Stub for the two transports that do not carry plain JSON: bulk
    downloads (stub_response.download) and error responses
    (stub_response.error), each armed separately from the JSON registry.

    Usage:
        def test_something(stub_response, load_fixture):
            stub_response("cards/named", load_fixture("cards_named_black_lotus"))
            card = scrython.cards.Named(exact="Black Lotus")
            assert card.name == "Black Lotus"
    """
    stub = _Stub()

    # Patch the limiter's wait() itself so the bypass holds regardless of which
    # _rate_limiter_class an endpoint uses; SlowRateLimiter inherits wait, so one
    # patch covers every tier. (Patching the scrython.base.RateLimiter name does
    # not work: _rate_limiter_class captures the class object at import time.)
    with (
        patch.object(RateLimiter, "wait", lambda *_: None),
        patch("scrython.base.urlopen", side_effect=stub.open),
        patch("scrython.bulk_data.bulk_data_mixins.urlopen", side_effect=stub.open_download),
    ):
        yield stub


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


# Arms the seam for each double-faced capture in turn and hands back the card id
# plus the front-face image URL that payload carries. The URL has to come from
# the payload rather than a literal in the test body: image URIs carry a
# cache-busting suffix that drifts on every fixture refresh.
@pytest.fixture(
    params=["cards_by_id__transform", "cards_by_id__modal_dfc"],
    ids=["transform", "modal_dfc"],
)
def cards_by_id__dfc_front_image(request, stub_response, load_fixture):
    payload = load_fixture(request.param)
    stub_response("cards/id", payload)
    return payload["id"], payload["card_faces"][0]["image_uris"]["normal"]


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
    stub_response.download(_SAMPLE_BULK_CARDS)


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


# The manifest capture is page one of /cards/manifest, truncated to two rows.
# Scryfall serves oracle_id, created_at and data_updated_at as null on every row
# it currently returns, so the second row is the captured row with those three
# filled in: one row exactly as captured, one doctored to reach the accessors the
# live payload leaves empty. Which cards land in the capture drifts on refresh,
# so the fixture hands both rows back for tests to read their values from.
_MANIFEST_POPULATED_FIELDS: dict = {
    "oracle_id": "e9c1d0b6-4a2f-4d18-8e73-5b6a0f9c2d14",
    "created_at": "2007-10-12T00:00:00Z",
    "data_updated_at": "2026-08-01T09:14:22Z",
}


@pytest.fixture
def cards_manifest__page_one(stub_response, load_fixture):
    """Arm `cards/manifest` with one captured row and one doctored row, and return both."""
    payload = load_fixture("cards_manifest__page_one")
    captured_row, second_row = payload["data"]
    doctored_row = {**second_row, **_MANIFEST_POPULATED_FIELDS}

    stub_response("cards/manifest", {**payload, "data": [captured_row, doctored_row]})
    return captured_row, doctored_row


def _manifest_row_for(card: dict, id_override: str | None = None) -> dict:
    """Build the thin manifest view of a captured card payload."""
    return {
        "id": id_override or card["id"],
        "oracle_id": card.get("oracle_id"),
        "name": card["name"],
        "set_code": card["set"],
        "collector_number": card["collector_number"],
        "lang": card["lang"],
    }


def _arm_manifest_and_search(stub_response, row: dict, card: dict) -> None:
    """Arm one manifest page and one search page carrying the full card.

    Search is the counterpart here because its list items are full `Object`
    cards, which is the comparison under test.
    """
    stub_response(
        "cards/manifest",
        {"object": "list", "has_more": False, "total_cards": 1, "data": [row]},
    )
    stub_response(
        "cards/search",
        {"object": "list", "has_more": False, "total_cards": 1, "data": [card]},
    )


@pytest.fixture
def cards_manifest__row_and_card_same_printing(stub_response, load_fixture):
    """Serve a manifest row and the full card object for one printing."""
    card = load_fixture("cards_named__black_lotus")
    _arm_manifest_and_search(stub_response, _manifest_row_for(card), card)


@pytest.fixture
def cards_manifest__row_and_card_different_printings(stub_response, load_fixture):
    """Serve a manifest row and a full card object carrying different IDs."""
    card = load_fixture("cards_named__black_lotus")
    row = _manifest_row_for(card, id_override="ffffffff-0000-4000-8000-ffffffffffff")
    _arm_manifest_and_search(stub_response, row, card)


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


# Scryfall answers an unmatched card name with 404 and this body. Synthetic
# because the capture script refuses to write a payload whose object is "error".
_NOT_FOUND_ERROR: dict = {
    "object": "error",
    "code": "not_found",
    "status": 404,
    "details": "No cards found matching “Chandra Nalaar, Pyromaster”",
    "warnings": ["Did you mean Chandra Nalaar?"],
}


@pytest.fixture
def cards_named__not_found_error(stub_response):
    """Arm `cards/named` to fail the way Scryfall fails an unmatched exact name."""
    stub_response.error(404, _NOT_FOUND_ERROR)
