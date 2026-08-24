# Sweep Fixture Corpus

## Selection criterion

Every fixture in this directory exists to give the property sweep engine
a payload that contains a specific Scryfall API field.  Fixtures are chosen
so that, collectively, every non-trivial `@property` accessor across every
mixin is exercised by at least one fixture — including optional fields that
appear only on certain card types (vanguard, battle, attraction, …) and
fields that appear only on individual faces of multi-faced cards.

This corpus is intentionally independent of the usage fixture corpus in
`tests/usage/fixtures/`.  The two corpora are selected under different
pressures and must not be coupled: a fixture refresh in one corpus must
not silently break the other.

## Corpus contents (33 fixtures)

### Card layout pins (12)

The 12 layout pins from the usage corpus, re-captured independently.
Full duplication is intended — the corpora must be able to drift apart
as they are refreshed and extended under their respective pressures.

| Fixture | Layout | Endpoint |
|---|---|---|
| `cards_named__black_lotus` | normal | `cards/named` |
| `cards_by_id__normal` | normal | `cards/id` |
| `cards_by_id__transform` | transform | `cards/id` |
| `cards_by_id__modal_dfc` | modal_dfc | `cards/id` |
| `cards_by_id__split` | split | `cards/id` |
| `cards_by_id__adventure` | adventure | `cards/id` |
| `cards_by_id__saga` | saga | `cards/id` |
| `cards_by_id__meld` | meld | `cards/id` |
| `cards_by_id__flip` | flip | `cards/id` |
| `cards_by_id__leveler` | leveler | `cards/id` |
| `cards_by_id__class` | class | `cards/id` |
| `cards_by_id__token` | token | `cards/id` |

### Card accessor pins (11)

One card per accessor group not reliably covered by the layout corpus.

Single-faced pins carry `-is:dfc` so the target field lands on the card itself
rather than only on one of its faces; the face pins below cover that side.

| Fixture | Discovery query | Covered fields |
|---|---|---|
| `cards_by_id__vanguard` | `t:vanguard order:released dir:asc` | `hand_modifier`, `life_modifier`, `promo_types` |
| `cards_by_id__japanese` | `lang:ja year>=2020 -is:dfc order:released dir:asc include_multilingual=true` | `printed_name`, `printed_text`, `printed_type_line` |
| `cards_by_id__attraction` | `t:attraction order:released dir:asc` | `attraction_lights` |
| `cards_by_id__indicator` | `has:indicator -is:dfc order:released dir:asc` | `color_indicator` |
| `cards_by_id__content_warning` | `is:contentwarning order:released dir:asc` | `content_warning` |
| `cards_by_id__battle` | `t:battle -is:dfc order:released dir:asc` | `defense` |
| `cards_by_id__flavor_name` | `has:flavorname -is:dfc order:released dir:asc` | `flavor_name` |
| `cards_by_id__planeswalker` | `t:planeswalker -is:dfc order:released dir:asc` | `loyalty` |
| `cards_by_id__etched` | `is:etched order:released dir:asc` | `tcgplayer_etched_id` |
| `cards_by_id__variation` | `is:variation order:released dir:asc` | `variation_of` |
| `cards_by_id__watermark` | `has:watermark -is:dfc order:released dir:asc` | `watermark` |

Japanese pins need `include_multilingual=true`; without it Scryfall search
returns only English printings, which carry no `printed_*` fields.

### Card face accessor pins (4)

Cards chosen because their `card_faces` array contains the target field.

| Fixture | Discovery query | Covered fields (on `card_faces`) |
|---|---|---|
| `cards_by_id__reversible` | `is:reversible order:released dir:asc` | `cmc`, `layout`, `oracle_id` |
| `cards_by_id__battle_dfc` | `t:battle is:dfc order:released dir:asc` | `defense` |
| `cards_by_id__planeswalker_transform` | `t:planeswalker is:transform order:released dir:asc` | `loyalty` |
| `cards_by_id__japanese_dfc` | `lang:ja is:dfc year>=2020 order:released dir:asc include_multilingual=true` | `printed_name`, `printed_text`, `printed_type_line` |

### Non-card fixtures (6)

| Fixture | Purpose |
|---|---|
| `sets_by_code__onc` | Set object; ONC covers 21/21 set accessors (LEA in usage covers 14) |
| `bulk_data_by_id__oracle_cards` | Bulk-data object |
| `catalogs_creature_types` | Catalog envelope |
| `cards_search__lea_red` | List envelope covering `has_more` and `total_cards` (`q=set:lea c:red cmc>=6`, one card) |
| `cards_search__mana_t_warning` | List envelope covering `warnings` (`q=set:lea c:red cmc>=6 mana:{T}`) |
| `cards_search__paginated` | List envelope covering `next_page` (truncated; see below) |

`mana:{T}` alone is a 400 — Scryfall ignores every term and returns an error
object, not a list.  Appended to valid terms it returns 200 and reports the
ignored term in `warnings`, which is what this fixture needs to cover.

`/sets` is not captured — 1047 objects / 621 KB; the set spec item corpus
comes from the single set object (`sets_by_code__onc`).

## Provenance format

Every fixture is a JSON object with two top-level keys:

```json
{
  "_provenance": {
    "captured_at": "<ISO 8601 UTC timestamp>",
    "endpoint": "<Scryfall endpoint label>",
    "source_url": "<full URL that was fetched>",
    "discovered_via": "<query or method used to identify this pin>",
    "scryfall_id": "<UUID, when the response has an id field>",
    "truncated_to": 2
  },
  "payload": { ... }
}
```

`truncated_to` appears only on `cards_search__paginated`, where the `data`
array was trimmed to preserve `has_more: true` and `next_page` while keeping
the file small.  All other fixtures are stored verbatim as returned by the API.

## Refreshing the corpus

Run the capture script to re-pull all sweep fixtures from the live Scryfall API:

```bash
python scripts/capture_fixtures.py sweep
```

To refresh a single fixture:

```bash
python scripts/capture_fixtures.py sweep cards_by_id__vanguard
```

Each card is pinned by its Scryfall UUID.  The `discovered_via` field in the
fixture's `_provenance` records the search query that originally located it,
so a pin can be re-derived by running that query on Scryfall and taking the
first result's `id`.

Scryfall enforces a 10 req/s rate limit; the capture script pauses 110 ms
between requests to stay within budget.
