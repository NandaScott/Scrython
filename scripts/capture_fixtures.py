#!/usr/bin/env python3
"""
Capture Scryfall API fixtures with provenance metadata.

Each fixture is stored as a JSON file with a `_provenance` header
(captured_at, endpoint, source_url, and scryfall_id when available)
alongside the raw Scryfall payload.

Run: python scripts/capture_fixtures.py
"""

import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SCRYFALL_API_BASE = "https://api.scryfall.com"

FIXTURES_DIR = Path(__file__).parent.parent / "tests" / "usage" / "fixtures"

# Declared map: fixture key → {endpoint, params}
# Pin cards by exact name so re-runs return the same canonical printing.
FIXTURE_MAP: dict[str, dict[str, str | dict[str, str]]] = {
    "cards_named_black_lotus": {
        "endpoint": "cards/named",
        "params": {"exact": "Black Lotus"},
    },
}


def fetch(endpoint: str, params: dict[str, str]) -> tuple[dict, str]:
    """
    Fetch one endpoint from the Scryfall API.

    Returns (payload, source_url).
    """
    query = urllib.parse.urlencode(params)
    url = f"{SCRYFALL_API_BASE}/{endpoint}?{query}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Scrython/dev (fixture-capture)"},
    )
    with urllib.request.urlopen(req) as response:
        payload: dict = json.loads(response.read().decode("utf-8"))
    return payload, url


def write_fixture(key: str, endpoint: str, source_url: str, payload: dict) -> None:
    """Write a fixture JSON file with a provenance envelope."""
    provenance: dict[str, str] = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "endpoint": endpoint,
        "source_url": source_url,
    }
    scryfall_id = payload.get("id")
    if isinstance(scryfall_id, str):
        provenance["scryfall_id"] = scryfall_id

    fixture = {
        "_provenance": provenance,
        "payload": payload,
    }

    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIXTURES_DIR / f"{key}.json"
    with open(output_path, "w") as f:
        json.dump(fixture, f, indent=2)
    print(f"  wrote {output_path}")


def main() -> None:
    for key, spec in FIXTURE_MAP.items():
        endpoint = str(spec["endpoint"])
        params = {k: str(v) for k, v in spec["params"].items()}  # type: ignore[union-attr]
        print(f"Capturing {key} ...")
        payload, source_url = fetch(endpoint, params)
        write_fixture(key, endpoint, source_url, payload)
        print(f"  name={payload.get('name', '(no name)')}, id={payload.get('id', '(no id)')}")


if __name__ == "__main__":
    main()
