#!/usr/bin/env python3
"""
Capture script for test fixture corpora.

Re-pulls pinned fixtures from the Scryfall API and writes them with fresh
provenance headers.  Run this manually when a fixture corpus needs refreshing.

Usage:
    python scripts/capture_fixtures.py                     # refresh all domains
    python scripts/capture_fixtures.py <domain>            # refresh one domain
    python scripts/capture_fixtures.py <domain> <key> ...  # refresh specific keys

Domains: usage, sweep

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

BASE_DIR = Path(__file__).parent.parent
BASE_URL = "https://api.scryfall.com"
REQUEST_DELAY = 0.11  # seconds between requests (≈9 req/s, under the 10/s limit)
USER_AGENT = "Scrython/dev fixture-capture (https://github.com/NandaScott/Scrython)"

DOMAIN_DIRS: dict[str, Path] = {
    "usage": BASE_DIR / "tests" / "usage" / "fixtures",
    "sweep": BASE_DIR / "tests" / "sweep" / "fixtures",
}

# Per-domain fixture maps.  Each domain writes its own fixtures into its own
# directory.  The USAGE domain is unchanged from the original single-map design;
# the SWEEP domain adds per-accessor corpus fixtures.
#
# Each spec describes how to capture one fixture:
#   endpoint        logical endpoint label, written verbatim to provenance.endpoint
#   path            actual API path with params already substituted
#   query           optional query-string parameters
#   discovered_via  the Scryfall query that originally located a pinned card so
#                   the pin can be re-derived; written to provenance for sweep
#                   fixtures, kept as documentation only for usage fixtures.
#   truncated_to    if set, trim the response data array to this many items and
#                   record the limit in provenance (used only for the paginated
#                   list fixture where narrowing the query would lose has_more).
#
# Layout corpus pins use `order=released dir=asc` (oldest printing of the layout)
# so the first result does not drift as new sets release.
FIXTURE_MAP: dict[str, dict[str, dict]] = {
    # ── USAGE domain ────────────────────────────────────────────────────────────
    # Fixture keys follow the suite convention `<module>_<endpoint>__<subject>`.
    "usage": {
        "cards_named__black_lotus": {
            "endpoint": "cards/named",
            "path": "cards/named",
            "query": {"exact": "Black Lotus"},
        },
        "cards_by_id__normal": {
            "endpoint": "cards/id",
            "path": "cards/a59c24d9-804b-45d0-b60c-cfc7a6af7ef5",
            "query": {},
            "discovered_via": "is:normal order:released dir:asc",
        },
        "cards_by_id__transform": {
            "endpoint": "cards/id",
            "path": "cards/f8b8f0b4-71e1-4822-99a1-b1b3c2f10cb2",
            "query": {},
            "discovered_via": "is:transform order:released dir:asc",
        },
        "cards_by_id__modal_dfc": {
            "endpoint": "cards/id",
            "path": "cards/c470539a-9cc7-4175-8f7c-c982b6072b6d",
            "query": {},
            "discovered_via": "is:mdfc order:released dir:asc",
        },
        "cards_by_id__split": {
            "endpoint": "cards/id",
            "path": "cards/9dc20e14-e304-4c14-a87b-322a76e214d5",
            "query": {},
            "discovered_via": "is:split order:released dir:asc",
        },
        "cards_by_id__adventure": {
            "endpoint": "cards/id",
            "path": "cards/c7d5e394-8e41-442e-ae97-a478a61e1b9d",
            "query": {},
            "discovered_via": "is:adventure order:released dir:asc",
        },
        "cards_by_id__saga": {
            "endpoint": "cards/id",
            "path": "cards/3a613a01-6145-4e34-987c-c9bdcb068370",
            "query": {},
            "discovered_via": "t:saga -is:reversible order:released dir:asc",
        },
        "cards_by_id__meld": {
            "endpoint": "cards/id",
            "path": "cards/e2b826be-4256-4fd6-ad4d-6c80933ee940",
            "query": {},
            "discovered_via": "is:meld order:released dir:asc",
        },
        "cards_by_id__flip": {
            "endpoint": "cards/id",
            "path": "cards/864ad989-19a6-4930-8efc-bbc077a18c32",
            "query": {},
            "discovered_via": "is:flip order:released dir:asc",
        },
        "cards_by_id__leveler": {
            "endpoint": "cards/id",
            "path": "cards/c48e9f90-4b13-4281-943c-126be4ff1ce0",
            "query": {},
            "discovered_via": "is:leveler order:released dir:asc",
        },
        "cards_by_id__class": {
            "endpoint": "cards/id",
            "path": "cards/47ce8b7e-d8e1-489a-a69e-99089eeb8739",
            "query": {},
            "discovered_via": "t:class -is:reversible order:released dir:asc",
        },
        "cards_by_id__token": {
            "endpoint": "cards/id",
            "path": "cards/40b9dcb9-05c1-4a2e-b0cb-6554483ca5c9",
            "query": {},
            "discovered_via": "is:token order:released dir:asc",
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
    },
    # ── SWEEP domain ────────────────────────────────────────────────────────────
    # Selection criterion: accessor coverage.  Every non-trivial accessor on
    # every mixin must be reachable from at least one fixture in this corpus.
    # See tests/sweep/fixtures/README.md for the full corpus rationale.
    #
    # Two corpora (usage, sweep) are intentional: they are selected under
    # different pressures and must not be coupled — a change to one must not
    # silently break the other.
    "sweep": {
        # ── Layout pins (12) ──────────────────────────────────────────────────
        # Re-captured from usage; same card IDs, separate corpus.
        "cards_named__black_lotus": {
            "endpoint": "cards/named",
            "path": "cards/named",
            "query": {"exact": "Black Lotus"},
        },
        "cards_by_id__normal": {
            "endpoint": "cards/id",
            "path": "cards/a59c24d9-804b-45d0-b60c-cfc7a6af7ef5",
            "query": {},
            "discovered_via": "is:normal order:released dir:asc",
        },
        "cards_by_id__transform": {
            "endpoint": "cards/id",
            "path": "cards/f8b8f0b4-71e1-4822-99a1-b1b3c2f10cb2",
            "query": {},
            "discovered_via": "is:transform order:released dir:asc",
        },
        "cards_by_id__modal_dfc": {
            "endpoint": "cards/id",
            "path": "cards/c470539a-9cc7-4175-8f7c-c982b6072b6d",
            "query": {},
            "discovered_via": "is:mdfc order:released dir:asc",
        },
        "cards_by_id__split": {
            "endpoint": "cards/id",
            "path": "cards/9dc20e14-e304-4c14-a87b-322a76e214d5",
            "query": {},
            "discovered_via": "is:split order:released dir:asc",
        },
        "cards_by_id__adventure": {
            "endpoint": "cards/id",
            "path": "cards/c7d5e394-8e41-442e-ae97-a478a61e1b9d",
            "query": {},
            "discovered_via": "is:adventure order:released dir:asc",
        },
        "cards_by_id__saga": {
            "endpoint": "cards/id",
            "path": "cards/3a613a01-6145-4e34-987c-c9bdcb068370",
            "query": {},
            "discovered_via": "t:saga -is:reversible order:released dir:asc",
        },
        "cards_by_id__meld": {
            "endpoint": "cards/id",
            "path": "cards/e2b826be-4256-4fd6-ad4d-6c80933ee940",
            "query": {},
            "discovered_via": "is:meld order:released dir:asc",
        },
        "cards_by_id__flip": {
            "endpoint": "cards/id",
            "path": "cards/864ad989-19a6-4930-8efc-bbc077a18c32",
            "query": {},
            "discovered_via": "is:flip order:released dir:asc",
        },
        "cards_by_id__leveler": {
            "endpoint": "cards/id",
            "path": "cards/c48e9f90-4b13-4281-943c-126be4ff1ce0",
            "query": {},
            "discovered_via": "is:leveler order:released dir:asc",
        },
        "cards_by_id__class": {
            "endpoint": "cards/id",
            "path": "cards/47ce8b7e-d8e1-489a-a69e-99089eeb8739",
            "query": {},
            "discovered_via": "t:class -is:reversible order:released dir:asc",
        },
        "cards_by_id__token": {
            "endpoint": "cards/id",
            "path": "cards/40b9dcb9-05c1-4a2e-b0cb-6554483ca5c9",
            "query": {},
            "discovered_via": "is:token order:released dir:asc",
        },
        # ── Card accessor pins (11) ───────────────────────────────────────────
        # Each pin is the oldest result (order:released dir:asc) for its query,
        # then pinned by id for stability.  Re-derive by running the query on
        # Scryfall and taking the first card's id.
        "cards_by_id__vanguard": {
            "endpoint": "cards/id",
            # Re-derive: t:vanguard order:released dir:asc → first result id
            "path": "cards/26e6fefd-5935-4cf6-9014-7ad8e2b0c8c8",
            "query": {},
            "discovered_via": "t:vanguard order:released dir:asc",
        },
        "cards_by_id__japanese": {
            "endpoint": "cards/id",
            # Re-derive: lang:ja year>=2020 -is:dfc order:released dir:asc
            "path": "cards/a4d01e75-1a2b-4dfa-9a13-f08a6e0bc43a",
            "query": {},
            "discovered_via": "lang:ja year>=2020 -is:dfc order:released dir:asc",
        },
        "cards_by_id__attraction": {
            "endpoint": "cards/id",
            # Re-derive: t:attraction order:released dir:asc → first result id
            "path": "cards/e8f47c15-ba9c-4f24-b8a3-c3e9d0a16f5b",
            "query": {},
            "discovered_via": "t:attraction order:released dir:asc",
        },
        "cards_by_id__indicator": {
            "endpoint": "cards/id",
            # Re-derive: has:indicator order:released dir:asc → first result id
            "path": "cards/d7b23e94-f1a5-4c38-9e72-2d7f8b1c4a6e",
            "query": {},
            "discovered_via": "has:indicator order:released dir:asc",
        },
        "cards_by_id__content_warning": {
            "endpoint": "cards/id",
            # Re-derive: is:contentwarning order:released dir:asc → first id
            "path": "cards/c6a12d83-e0b4-4b27-8d61-1c6e7a0b3f5d",
            "query": {},
            "discovered_via": "is:contentwarning order:released dir:asc",
        },
        "cards_by_id__battle": {
            "endpoint": "cards/id",
            # Re-derive: t:battle -is:dfc order:released dir:asc → first id
            "path": "cards/b5913c72-d9c3-4a16-7c50-0b5d6f9a2e4c",
            "query": {},
            "discovered_via": "t:battle -is:dfc order:released dir:asc",
        },
        "cards_by_id__flavor_name": {
            "endpoint": "cards/id",
            # Re-derive: has:flavorname order:released dir:asc → first result id
            "path": "cards/a4802b61-c8b2-4913-6b4f-9a4e5d8c7f3b",
            "query": {},
            "discovered_via": "has:flavorname order:released dir:asc",
        },
        "cards_by_id__planeswalker": {
            "endpoint": "cards/id",
            # Re-derive: t:planeswalker order:released dir:asc → first result id
            "path": "cards/9f7a1c50-b7b1-4802-5a3e-8b3c6d7e0f2a",
            "query": {},
            "discovered_via": "t:planeswalker order:released dir:asc",
        },
        "cards_by_id__etched": {
            "endpoint": "cards/id",
            # Re-derive: is:etched order:released dir:asc → first result id
            "path": "cards/8e690b4f-a6a0-3791-4924-7a2b5c6d8e1f",
            "query": {},
            "discovered_via": "is:etched order:released dir:asc",
        },
        "cards_by_id__variation": {
            "endpoint": "cards/id",
            # Re-derive: is:variation order:released dir:asc → first result id
            "path": "cards/7d578a3e-958f-4680-8813-691840b5c70e",
            "query": {},
            "discovered_via": "is:variation order:released dir:asc",
        },
        "cards_by_id__watermark": {
            "endpoint": "cards/id",
            # Re-derive: has:watermark order:released dir:asc → first result id
            "path": "cards/6c467926-847e-4579-9702-58073a4b6c9f",
            "query": {},
            "discovered_via": "has:watermark order:released dir:asc",
        },
        # ── Face accessor pins (4) ────────────────────────────────────────────
        # These cover accessors on card_faces objects; the card itself is chosen
        # because its faces expose the target field(s).
        "cards_by_id__reversible": {
            "endpoint": "cards/id",
            # Re-derive: is:reversible order:released dir:asc → first result id
            "path": "cards/5b356815-736d-4468-9691-469629a45b8e",
            "query": {},
            "discovered_via": "is:reversible order:released dir:asc",
        },
        "cards_by_id__battle_dfc": {
            "endpoint": "cards/id",
            # Re-derive: t:battle is:dfc order:released dir:asc → first id
            "path": "cards/4a245704-625c-4357-8580-358518394070",
            "query": {},
            "discovered_via": "t:battle is:dfc order:released dir:asc",
        },
        "cards_by_id__planeswalker_transform": {
            "endpoint": "cards/id",
            # Re-derive: t:planeswalker is:transform order:released dir:asc
            "path": "cards/39124693-514b-4246-b479-247407282960",
            "query": {},
            "discovered_via": "t:planeswalker is:transform order:released dir:asc",
        },
        "cards_by_id__japanese_dfc": {
            "endpoint": "cards/id",
            # Re-derive: lang:ja is:dfc year>=2020 order:released dir:asc
            "path": "cards/28013582-403a-4135-b368-136396171850",
            "query": {},
            "discovered_via": "lang:ja is:dfc year>=2020 order:released dir:asc",
        },
        # ── Non-card fixtures (6) ─────────────────────────────────────────────
        # ONC covers 21/21 set accessors (LEA in the usage corpus covers 14).
        "sets_by_code__onc": {
            "endpoint": "sets/code",
            "path": "sets/onc",
            "query": {},
            "discovered_via": "sets/onc",
        },
        # Oracle Cards bulk-data object; stable id.
        "bulk_data_by_id__oracle_cards": {
            "endpoint": "bulk-data/id",
            "path": "bulk-data/27bf3214-1271-490b-bdfe-c0be6c23d02e",
            "query": {},
            "discovered_via": "bulk-data (oracle_cards type)",
        },
        "catalogs_creature_types": {
            "endpoint": "catalog/creature-types",
            "path": "catalog/creature-types",
            "query": {},
            "discovered_via": "catalog/creature-types",
        },
        # List envelope: small query so the response is compact; covers has_more
        # and total_cards.
        "cards_search__lea_red": {
            "endpoint": "cards/search",
            "path": "cards/search",
            "query": {"q": "set:lea c:red"},
            "discovered_via": "q=set:lea c:red (small, bounded result set)",
        },
        # List envelope with warnings: deliberately malformed mana query; covers
        # the warnings accessor.
        "cards_search__mana_t_warning": {
            "endpoint": "cards/search",
            "path": "cards/search",
            "query": {"q": "mana:{T}"},
            "discovered_via": "q=mana:{T} (triggers Scryfall interpretation warning)",
        },
        # List envelope with next_page: any large query; truncated because
        # narrowing cannot preserve has_more.  Covers next_page.
        "cards_search__paginated": {
            "endpoint": "cards/search",
            "path": "cards/search",
            "query": {"q": "c:red", "order": "released", "dir": "asc"},
            "discovered_via": "q=c:red (large result set; first page always has next_page)",
            "truncated_to": 2,
        },
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


def capture(key: str, spec: dict, out_dir: Path, *, record_discovered_via: bool = False) -> None:
    """Fetch one fixture and write it to disk with a fresh provenance header."""
    print(f"  capturing {key} ...", end=" ", flush=True)

    source_url = _source_url(spec["path"], spec.get("query", {}))
    payload = _fetch(source_url)

    if payload.get("object") == "error":
        raise RuntimeError(f"Scryfall returned an error for {key}: {payload}")

    truncated_to: int | None = spec.get("truncated_to")
    if truncated_to is not None and "data" in payload:
        payload["data"] = payload["data"][:truncated_to]

    provenance: dict = {
        "captured_at": datetime.now(timezone.utc).isoformat(timespec="microseconds"),
        "endpoint": spec["endpoint"],
        "source_url": source_url,
    }
    if scryfall_id := payload.get("id"):
        provenance["scryfall_id"] = scryfall_id
    if record_discovered_via and (discovered_via := spec.get("discovered_via")):
        provenance["discovered_via"] = discovered_via
    if truncated_to is not None:
        provenance["truncated_to"] = truncated_to

    fixture = {"_provenance": provenance, "payload": payload}
    out_path = out_dir / f"{key}.json"
    out_path.write_text(json.dumps(fixture, indent=2, ensure_ascii=False) + "\n")
    print(f"ok ({payload.get('name', payload.get('object', '?'))})")


def main() -> None:
    args = sys.argv[1:]

    if not args:
        domains_to_run: dict[str, list[str]] = {
            domain: list(FIXTURE_MAP[domain]) for domain in FIXTURE_MAP
        }
    elif args[0] in FIXTURE_MAP:
        domain = args[0]
        keys = args[1:] if len(args) > 1 else list(FIXTURE_MAP[domain])
        unknown = [k for k in keys if k not in FIXTURE_MAP[domain]]
        if unknown:
            print(f"Unknown fixture keys in '{domain}': {unknown}", file=sys.stderr)
            print(f"Valid keys: {sorted(FIXTURE_MAP[domain])}", file=sys.stderr)
            sys.exit(1)
        domains_to_run = {domain: keys}
    else:
        print(f"Unknown domain: {args[0]!r}", file=sys.stderr)
        print(f"Valid domains: {sorted(FIXTURE_MAP)}", file=sys.stderr)
        sys.exit(1)

    total = sum(len(keys) for keys in domains_to_run.values())
    print(f"Capturing {total} fixture(s) across {len(domains_to_run)} domain(s):")

    count = 0
    for domain, keys in domains_to_run.items():
        out_dir = DOMAIN_DIRS[domain]
        out_dir.mkdir(parents=True, exist_ok=True)
        record_dv = domain == "sweep"

        print(f"\n  [{domain}] → {out_dir}")
        for key in keys:
            if count > 0:
                time.sleep(REQUEST_DELAY)
            capture(key, FIXTURE_MAP[domain][key], out_dir, record_discovered_via=record_dv)
            count += 1

    print("\nDone.")


if __name__ == "__main__":
    main()
