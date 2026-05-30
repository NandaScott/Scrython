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
| `mock_urlopen.calls[0]["url"]` | Request URL — implementation detail of the `urlopen` seam |
| Patch objects of any kind | Seam internals leak through |

```python
# correct
assert card.name == "Black Lotus"

# wrong — asserts against internal state
assert card.scryfall_data.name == "Black Lotus"

# wrong — inspects the mock seam
assert "exact=Black+Lotus" in mock_urlopen.calls[0]["url"]
```

## 3. Assert stable identity fields, not volatile ones

Some fields change between fixture refreshes (prices, `updated_at`, print
counts).  Assertions must target stable identity fields that do not drift:

| Stable (assert these) | Volatile (exclude) |
|---|---|
| `name`, `mana_cost`, `type_line` | `prices` |
| `oracle_text`, `set`, `set_name` | `updated_at`, `size` |
| `id` (when testing a by-ID endpoint) | any field that changes per-printing |

A fixture refresh should never redden the suite.

## 4. Route all mocking through `stub_response`

`stub_response` (defined in `tests/usage/conftest.py`) is the only fixture
that touches the mock seam.  Every usage test that needs a stubbed HTTP
response must go through it:

```python
def test_named_exact_returns_correct_name(stub_response, load_fixture):
    stub_response("cards/named", load_fixture("cards_named_black_lotus"))
    card = scrython.cards.Named(exact="Black Lotus")
    assert card.name == "Black Lotus"
```

Test bodies must not import or call `mock_urlopen`, `patch`, `urlopen`, or any
other mock primitive directly.

### Seam-isolation rationale

`stub_response` exists so that the entire usage suite can be migrated to the
`MockConnector` abstraction (issue #169) in a single, mechanical file change.
When #169 lands, only the body of `stub_response` in `conftest.py` changes
(swapped to `MockConnector` + `use_connector(...)`).  Every test body stays
identical because no test body knows which seam is in use.

If a test bypasses `stub_response` and calls the urlopen patch directly, it
will break during that migration and require a rewrite.

## Canonical template

`tests/usage/test_cards_named.py` (introduced in issue #183) is the
copyable template for every new usage test:

```python
"""Usage tests for scrython.cards.Named."""

import scrython.cards


def test_named_exact_returns_correct_name(stub_response, load_fixture):
    stub_response("cards/named", load_fixture("cards_named_black_lotus"))
    card = scrython.cards.Named(exact="Black Lotus")
    assert card.name == "Black Lotus"
```

This test demonstrates the full harness path:

1. `load_fixture` reads a committed JSON file from `tests/usage/fixtures/` by
   key (`cards_named_black_lotus` → `cards_named_black_lotus.json`).
2. `stub_response` registers that payload as the HTTP response for the
   `cards/named` endpoint.
3. The card is constructed via the dotted public path.
4. The assertion targets `card.name` — a stable public property.

No internals appear anywhere in the test body.
