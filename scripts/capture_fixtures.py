#!/usr/bin/env python3
"""
Capture script for usage test fixtures.

Re-pulls pinned fixtures from the Scryfall API and writes them with fresh
provenance headers.  Run this manually when the fixture corpus needs refreshing.

Usage:
    python scripts/capture_fixtures.py           # refresh all fixtures
    python scripts/capture_fixtures.py <key>     # refresh one fixture by key

Scryfall rate-limit: 10 requests/second; this script pauses 110 ms between
requests to stay comfortably within that budget.
"""

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent.parent / "tests" / "usage" / "fixtures"
BASE_URL = "https://api.scryfall.com"
REQUEST_DELAY = 0.11  # seconds between requests (≈9 req/s, under the 10/s limit)
USER_AGENT = "Scrython/dev fixture-capture (https://github.com/NandaScott/Scrython)"

# Declared map: fixture key → Scryfall request specification.
#
# Fixture keys follow the suite convention `<module>_<endpoint>__<subject>`, the
# same shape the tests and conftest fixtures use.
#
# Each spec describes how to capture one fixture:
#   endpoint        logical endpoint label, written verbatim to provenance.endpoint
#   path            actual API path with params already substituted
#   query           optional query-string parameters
#   discovered_via  documentation only (ignored at capture): the Scryfall search
#                   that originally resolved a pinned card id, so the pin can be
#                   re-derived. Layout cards use `order=released dir=asc` (oldest
#                   printing of the layout) so the first result does not drift as
#                   new sets release.
#
# Layout corpus: one card per Scryfall layout, discovered by `is:<layout>`
# (`t:<layout>` where no `is:` filter exists) and then pinned by id.
FIXTURE_MAP: dict[str, dict] = {
    "cards_named__black_lotus": {
        "endpoint": "cards/named",
        "path": "cards/named",
        "query": {"exact": "Black Lotus"},
    },
    "cards_by_id__normal": {
        "endpoint": "cards/id",
        "path": "cards/a59c24d9-804b-45d0-b60c-cfc7a6af7ef5",
        "query": {},
        "discovered_via": "is:normal",
    },
    "cards_by_id__transform": {
        "endpoint": "cards/id",
        "path": "cards/f8b8f0b4-71e1-4822-99a1-b1b3c2f10cb2",
        "query": {},
        "discovered_via": "is:transform",
    },
    "cards_by_id__modal_dfc": {
        "endpoint": "cards/id",
        "path": "cards/c470539a-9cc7-4175-8f7c-c982b6072b6d",
        "query": {},
        "discovered_via": "is:mdfc",
    },
    "cards_by_id__split": {
        "endpoint": "cards/id",
        "path": "cards/9dc20e14-e304-4c14-a87b-322a76e214d5",
        "query": {},
        "discovered_via": "is:split",
    },
    "cards_by_id__adventure": {
        "endpoint": "cards/id",
        "path": "cards/c7d5e394-8e41-442e-ae97-a478a61e1b9d",
        "query": {},
        "discovered_via": "is:adventure",
    },
    "cards_by_id__saga": {
        "endpoint": "cards/id",
        "path": "cards/3a613a01-6145-4e34-987c-c9bdcb068370",
        "query": {},
        "discovered_via": "t:saga -is:reversible",
    },
    "cards_by_id__meld": {
        "endpoint": "cards/id",
        "path": "cards/e2b826be-4256-4fd6-ad4d-6c80933ee940",
        "query": {},
        "discovered_via": "is:meld",
    },
    "cards_by_id__flip": {
        "endpoint": "cards/id",
        "path": "cards/864ad989-19a6-4930-8efc-bbc077a18c32",
        "query": {},
        "discovered_via": "is:flip",
    },
    "cards_by_id__leveler": {
        "endpoint": "cards/id",
        "path": "cards/c48e9f90-4b13-4281-943c-126be4ff1ce0",
        "query": {},
        "discovered_via": "is:leveler",
    },
    "cards_by_id__class": {
        "endpoint": "cards/id",
        "path": "cards/47ce8b7e-d8e1-489a-a69e-99089eeb8739",
        "query": {},
        "discovered_via": "t:class -is:reversible",
    },
    "cards_by_id__token": {
        "endpoint": "cards/id",
        "path": "cards/40b9dcb9-05c1-4a2e-b0cb-6554483ca5c9",
        "query": {},
        "discovered_via": "is:token",
    },
    "sets_by_code__lea": {
        "endpoint": "sets/code",
        "path": "sets/lea",
        "query": {},
    },
    # Oracle Cards bulk-data object; its id is stable across Scryfall refreshes.
    "bulk_data_by_id__oracle_cards": {
        "endpoint": "bulk-data/id",
        "path": "bulk-data/27bf3214-1271-490b-bdfe-c0be6c23d02e",
        "query": {},
    },
    "catalogs_creature_types": {
        "endpoint": "catalog/creature-types",
        "path": "catalog/creature-types",
        "query": {},
    },
    # Rulings for Rules Lawyer, a card whose whole identity is carrying rulings.
    "rulings_by_id__rules_lawyer": {
        "endpoint": "cards/id/rulings",
        "path": "cards/6c02c575-5685-44f5-8b47-89d888529d1b/rulings",
        "query": {},
    },
    "symbology_all": {
        "endpoint": "symbology",
        "path": "symbology",
        "query": {},
    },
    # Migrations are immutable historical records, so a specific id is stable.
    "migrations_by_id__merge": {
        "endpoint": "migrations/id",
        "path": "migrations/f75b2d8b-c73b-4352-91f7-3b9239bd3c9f",
        "query": {},
    },
}


def _source_url(path: str, query: dict) -> str:
    """Return the full URL for a path + query, matching what gets requested."""
    if query:
        return f"{BASE_URL}/{path}?{urllib.parse.urlencode(query)}"
    return f"{BASE_URL}/{path}"


def _fetch(url: str) -> dict:
    """GET a Scryfall URL and return the parsed JSON body."""
    request = urllib.request.Request(url)
    request.add_header("User-Agent", USER_AGENT)
    request.add_header("Accept", "application/json")

    try:
        with urllib.request.urlopen(request) as response:
            charset = response.info().get_param("charset") or "utf-8"
            return json.loads(response.read().decode(charset))
    except urllib.error.HTTPError as exc:
        charset = exc.headers.get_param("charset")
        if not isinstance(charset, str):
            charset = "utf-8"
        error_body = exc.read().decode(charset)
        raise RuntimeError(f"HTTP {exc.code} from {url}: {error_body}") from exc


def capture(key: str, spec: dict) -> None:
    """Fetch one fixture and write it to disk with a fresh provenance header."""
    print(f"  capturing {key} ...", end=" ", flush=True)

    source_url = _source_url(spec["path"], spec.get("query", {}))
    payload = _fetch(source_url)

    if payload.get("object") == "error":
        raise RuntimeError(f"Scryfall returned an error for {key}: {payload}")

    provenance: dict = {
        "captured_at": datetime.now(timezone.utc).isoformat(timespec="microseconds"),
        "endpoint": spec["endpoint"],
        "source_url": source_url,
    }
    if scryfall_id := payload.get("id"):
        provenance["scryfall_id"] = scryfall_id

    fixture = {"_provenance": provenance, "payload": payload}
    out_path = FIXTURES_DIR / f"{key}.json"
    out_path.write_text(json.dumps(fixture, indent=2, ensure_ascii=False) + "\n")
    print(f"ok ({payload.get('name', payload.get('object', '?'))})")


def main() -> None:
    keys_to_run = sys.argv[1:] if len(sys.argv) > 1 else list(FIXTURE_MAP)

    unknown = [k for k in keys_to_run if k not in FIXTURE_MAP]
    if unknown:
        print(f"Unknown fixture keys: {unknown}", file=sys.stderr)
        print(f"Valid keys: {sorted(FIXTURE_MAP)}", file=sys.stderr)
        sys.exit(1)

    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Capturing {len(keys_to_run)} fixture(s) into {FIXTURES_DIR}:")

    for index, key in enumerate(keys_to_run):
        if index > 0:
            time.sleep(REQUEST_DELAY)
        capture(key, FIXTURE_MAP[key])

    print("Done.")


if __name__ == "__main__":
    main()
