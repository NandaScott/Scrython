# USAGE Suite Conventions

This document codifies the rules every test in `tests/usage/` must follow to
stay honestly black-box and remain maintainable across future seam changes.

## 1. Construct via the dotted public path

Instantiate endpoint classes using the same dotted path a README user would
type — not a bare-import alias:

```python
# correct
import scrython.cards
card = scrython.cards.Named(exact="Black Lotus")

# wrong — bare import couples the test to the internal module layout
from scrython.cards import Named
card = Named(exact="Black Lotus")
```

This ensures tests exercise the same surface documented for users and survive
internal restructuring.

## 2. Assert only on the public API

Assert against public properties and public methods.  The following are
internal implementation details and must not appear in test bodies:

| Forbidden | Why |
|---|---|
| `card.scryfall_data` | Internal parsed-response object |
| `card._scryfall_data` | Private attribute |
| The requested URL or endpoint | Request routing — implementation detail of the mock seam |
| Patch objects of any kind | Seam internals leak through |

```python
# correct
assert card.name == "Black Lotus"

# wrong — asserts against internal state
assert card.scryfall_data.name == "Black Lotus"

# wrong — inspects the mock seam
assert "exact=Black+Lotus" in requested_url
```

## 3. Assert stable identity fields, not volatile values

Some field *values* change between fixture refreshes (prices, `updated_at`, print
counts).  Assertions must target stable identity fields whose values do not drift:

| Stable (assert these) | Volatile (exclude) |
|---|---|
| `name`, `mana_cost`, `type_line` | `prices` |
| `oracle_text`, `set`, `set_name` | `updated_at`, `size` |
| `id` (when testing a by-ID endpoint) | any field that changes per-printing |

A fixture refresh should never redden the **usage** suite.

New or removed *keys* are a different matter: the property sweep's reverse
coverage guard (in `tests/sweep/`) is designed to redden when Scryfall adds or
removes a top-level field.  A guard failure after a fixture refresh is not a
regression — it is the guard doing its job.  Add the missing accessor (or alias
or wrapper entry) to clear it.

## 4. Arm the seam through an injected payload fixture

`stub_response` (defined in `tests/usage/conftest.py`) is the only fixture that
touches the mock seam. Tests do not call it directly; instead `conftest.py`
exposes one **payload fixture** per captured fixture — named the same as the
fixture key — that arms `stub_response` with the right endpoint and payload. A
test requests that fixture by name and then constructs through the public API:

```python
def test_named__exact__returns_correct_name(cards_named__black_lotus):
    card = scrython.cards.Named(exact="Black Lotus")
    assert card.name == "Black Lotus"
```

The fixture parameter is intentionally unreferenced — requesting it is what
registers the payload (`tests/usage/test_*.py` ignores `ARG001` for this).
Test bodies must not import or call `patch`, `urlopen`, `stub_response`, or
`load_fixture` directly.

### Seam-isolation rationale

`stub_response` exists so that the entire usage suite can be migrated to the
`MockConnector` abstraction (issue #169) in a single, mechanical file change.
When #169 lands, only the body of `stub_response` in `conftest.py` changes
(swapped to `MockConnector` + `use_connector(...)`). Every test body stays
identical because no test body knows which seam is in use.

If a test bypasses the payload fixtures and drives the seam directly, it will
break during that migration and require a rewrite.

## 5. Name tests and fixtures by `endpoint`, `query`, `scenario`

- **Tests:** `test_<endpoint>__<query>__<scenario>` — double underscore between
  segments. `endpoint` is the public class lowered (`Named` → `named`, `ById` →
  `by_id`, `ByCode` → `by_code`); `query` is the selector used (`exact`, `id`,
  `code`, `rulings`); `scenario` is what is asserted
  (`returns_correct_name`, `has_saga_layout`).
- **Fixtures and fixture keys:** `<module>_<endpoint>__<subject>`
  (`cards_named__black_lotus`, `rulings_by_id__rules_lawyer`). The committed
  JSON file, the `FIXTURE_MAP` key in `scripts/capture_fixtures.py`, and the
  injected conftest fixture all share this one name.

## 6. Pin the layout corpus by discovered id

The layout corpus pins one card per Scryfall `layout`. Each is discovered with
`is:<layout>` (`t:<layout>` where no `is:` filter exists), ordered
`released asc` so the first result does not drift as new sets release, and then
**pinned by id** in `FIXTURE_MAP` (the `discovered_via` note records the query).
Corpus tests fetch via `scrython.cards.ById` and assert only `layout`.

## Canonical template

`tests/usage/test_cards_named.py` is the copyable template for every new usage
test:

```python
"""Usage tests for scrython.cards.Named."""

import scrython.cards


def test_named__exact__returns_correct_name(cards_named__black_lotus):
    card = scrython.cards.Named(exact="Black Lotus")
    assert card.name == "Black Lotus"
```

This demonstrates the full harness path:

1. The `cards_named__black_lotus` payload fixture (in `conftest.py`) calls
   `load_fixture("cards_named__black_lotus")` and arms `stub_response` for the
   `cards/named` endpoint.
2. The card is constructed via the dotted public path.
3. The assertion targets `card.name` — a stable public property.

No internals appear anywhere in the test body.
