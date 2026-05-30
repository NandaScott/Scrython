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
# One entry per card layout so every structurally-distinct card shape is covered.
# To pin a different card for a layout, change the params dict here and re-run.
#
# layout       card                                         source endpoint
# ----------   ------------------------------------------   ---------------
# normal       Black Lotus (LEA)                            cards/named
# transform    Delver of Secrets // Insectile Aberration    cards/named
# modal_dfc    Emeria's Call // Emeria, Shattered Skyclave  cards/named
# split        Fire // Ice (APC)                            cards/named
# adventure    Bonecrusher Giant // Stomp (ELD)             cards/named
# saga         The Binding of the Old Gods (KHM)            cards/named
# meld         Gisela, the Broken Blade (EMN)               cards/named
# flip         Nezumi Shortfang // Stabwhisker the Odious   cards/named
# leveler      Transcendent Master (ROE)                    cards/named
# class        Fighter Class (AFR)                          cards/named
# token        Zombie token (Innistrad: Midnight Hunt)      cards/id (tokens need ID)
FIXTURE_MAP: dict[str, dict] = {
    "cards_named_black_lotus": {
        "endpoint": "cards/named",
        "params": {"exact": "Black Lotus"},
    },
    "cards_layout_transform": {
        "endpoint": "cards/named",
        "params": {
            "exact": "Delver of Secrets // Insectile Aberration",
            "set": "isd",
        },
    },
    "cards_layout_modal_dfc": {
        "endpoint": "cards/named",
        "params": {
            "exact": "Emeria's Call // Emeria, Shattered Skyclave",
            "set": "znr",
        },
    },
    "cards_layout_split": {
        "endpoint": "cards/named",
        "params": {"exact": "Fire // Ice", "set": "apc"},
    },
    "cards_layout_adventure": {
        "endpoint": "cards/named",
        "params": {"exact": "Bonecrusher Giant // Stomp", "set": "eld"},
    },
    "cards_layout_saga": {
        "endpoint": "cards/named",
        "params": {"exact": "The Binding of the Old Gods", "set": "khm"},
    },
    "cards_layout_meld": {
        "endpoint": "cards/named",
        "params": {"exact": "Gisela, the Broken Blade", "set": "emn"},
    },
    "cards_layout_flip": {
        "endpoint": "cards/named",
        "params": {
            "exact": "Nezumi Shortfang // Stabwhisker the Odious",
            "set": "bok",
        },
    },
    "cards_layout_leveler": {
        "endpoint": "cards/named",
        "params": {"exact": "Transcendent Master", "set": "roe"},
    },
    "cards_layout_class": {
        "endpoint": "cards/named",
        "params": {"exact": "Fighter Class", "set": "afr"},
    },
    # Tokens cannot be found by name alone; pin by Scryfall ID instead.
    # The ID below is the 2/2 Black Zombie token from Innistrad: Midnight Hunt.
    "cards_layout_token": {
        "endpoint": "cards/id",
        "params": {"id": "a0f08f4f-49a7-4cd9-af67-b4d79b07ad3b"},
    },
}


def _fetch(endpoint: str, params: dict) -> dict:
    """Fetch a single card from Scryfall and return the parsed JSON body."""
    if endpoint == "cards/id":
        card_id = params["id"]
        url = f"{BASE_URL}/cards/{card_id}"
    else:
        query = urllib.parse.urlencode(params)
        url = f"{BASE_URL}/{endpoint}?{query}"

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


def _build_source_url(endpoint: str, params: dict) -> str:
    """Return the URL that was used to capture this fixture."""
    if endpoint == "cards/id":
        return f"{BASE_URL}/cards/{params['id']}"
    query = urllib.parse.urlencode(params)
    return f"{BASE_URL}/{endpoint}?{query}"


def capture(key: str, spec: dict) -> None:
    """Fetch one fixture and write it to disk with a fresh provenance header."""
    print(f"  capturing {key} ...", end=" ", flush=True)

    payload = _fetch(spec["endpoint"], spec["params"])

    if payload.get("object") == "error":
        raise RuntimeError(f"Scryfall returned an error for {key}: {payload}")

    provenance: dict = {
        "captured_at": datetime.now(timezone.utc).isoformat(timespec="microseconds"),
        "endpoint": spec["endpoint"],
        "source_url": _build_source_url(spec["endpoint"], spec["params"]),
    }
    if scryfall_id := payload.get("id"):
        provenance["scryfall_id"] = scryfall_id

    fixture = {"_provenance": provenance, "payload": payload}
    out_path = FIXTURES_DIR / f"{key}.json"
    out_path.write_text(json.dumps(fixture, indent=2, ensure_ascii=False) + "\n")
    print(f"ok ({payload.get('name', '?')})")


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
