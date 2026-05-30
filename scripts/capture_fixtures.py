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
# Each spec describes how to capture one fixture:
#   endpoint  logical endpoint label, written verbatim to provenance.endpoint
#   path      actual API path with params already substituted (e.g. "sets/lea");
#             omit for specs whose path is resolved at capture time (see dynamic)
#   query     optional query-string parameters
#   dynamic   optional resolver name for paths that depend on live data
#             ("migration": pin the first id returned by the /migrations list)
#
# Card layouts (one entry per structurally-distinct card shape):
#   normal Black Lotus · transform Delver of Secrets · modal_dfc Emeria's Call ·
#   split Fire // Ice · adventure Bonecrusher Giant · saga Binding of the Old Gods ·
#   meld Gisela · flip Nezumi Shortfang · leveler Transcendent Master ·
#   class Fighter Class · token Midnight Hunt Zombie (pinned by id; tokens
#   cannot be found by name alone).
FIXTURE_MAP: dict[str, dict] = {
    "cards_named_black_lotus": {
        "endpoint": "cards/named",
        "path": "cards/named",
        "query": {"exact": "Black Lotus"},
    },
    "cards_layout_transform": {
        "endpoint": "cards/named",
        "path": "cards/named",
        "query": {"exact": "Delver of Secrets // Insectile Aberration", "set": "isd"},
    },
    "cards_layout_modal_dfc": {
        "endpoint": "cards/named",
        "path": "cards/named",
        "query": {"exact": "Emeria's Call // Emeria, Shattered Skyclave", "set": "znr"},
    },
    "cards_layout_split": {
        "endpoint": "cards/named",
        "path": "cards/named",
        "query": {"exact": "Fire // Ice", "set": "apc"},
    },
    "cards_layout_adventure": {
        "endpoint": "cards/named",
        "path": "cards/named",
        "query": {"exact": "Bonecrusher Giant // Stomp", "set": "eld"},
    },
    "cards_layout_saga": {
        "endpoint": "cards/named",
        "path": "cards/named",
        "query": {"exact": "Binding the Old Gods", "set": "khm"},
    },
    "cards_layout_meld": {
        "endpoint": "cards/named",
        "path": "cards/named",
        "query": {"exact": "Gisela, the Broken Blade", "set": "emn"},
    },
    "cards_layout_flip": {
        "endpoint": "cards/named",
        "path": "cards/named",
        "query": {"exact": "Nezumi Shortfang // Stabwhisker the Odious", "set": "chk"},
    },
    "cards_layout_leveler": {
        "endpoint": "cards/named",
        "path": "cards/named",
        "query": {"exact": "Transcendent Master", "set": "roe"},
    },
    "cards_layout_class": {
        "endpoint": "cards/named",
        "path": "cards/named",
        "query": {"exact": "Fighter Class", "set": "afr"},
    },
    # The id below is the Zombie token from Innistrad: Midnight Hunt (tmid).
    "cards_layout_token": {
        "endpoint": "cards/id",
        "path": "cards/6adb8607-1066-451d-a719-74ad32358278",
        "query": {},
    },
    "sets_by_code_lea": {
        "endpoint": "sets/code",
        "path": "sets/lea",
        "query": {},
    },
    # Oracle Cards bulk-data object; its id is stable across Scryfall refreshes.
    "bulk_data_by_id": {
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
    "rulings_by_id": {
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
    "migrations_by_id": {
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
