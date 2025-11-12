# Scryfall API Implementation Checklist

This document tracks Scrython's implementation status for all Scryfall API endpoints.

**Last Updated:** 2025-01-11
**Scrython Version:** 2.0.0 (Rewrite Branch)

**Legend:**
- ✅ Fully implemented
- ❌ Not implemented

---

## Implementation Overview

| Category | Status | Coverage | Priority |
|----------|--------|----------|----------|
| Cards | ✅ Complete | 13/13 (100%) | - |
| Sets | ✅ Complete | 4/4 (100%) | - |
| Bulk Data | ✅ Complete | 3/3 (100%) | - |
| Rulings | ❌ Not Implemented | 0/5 (0%) | HIGH |
| Symbology | ❌ Not Implemented | 0/2 (0%) | MEDIUM |
| Catalogs | ⚠️ Partial | 1/20 (5%) | MEDIUM |
| Card Migrations | ❌ Not Implemented | 0/2 (0%) | LOW |

**Overall API Coverage: 21/49 endpoints (43%)**

---

## 1. Cards API ✅ COMPLETE

All 13 card endpoints are fully implemented with comprehensive property accessors.

### Endpoints

| Endpoint | Path | Class | Status |
|----------|------|-------|--------|
| Search Cards | `GET /cards/search` | `scrython.cards.Search` | ✅ |
| Named Card Lookup | `GET /cards/named` | `scrython.cards.Named` | ✅ |
| Card Autocomplete | `GET /cards/autocomplete` | `scrython.cards.Autocomplete` | ✅ |
| Random Card | `GET /cards/random` | `scrython.cards.Random` | ✅ |
| Card Collection | `POST /cards/collection` | `scrython.cards.Collection` | ✅ |
| By Set Code & Number | `GET /cards/:code/:number(/:lang)` | `scrython.cards.ByCodeNumber` | ✅ |
| By Multiverse ID | `GET /cards/multiverse/:id` | `scrython.cards.ByMultiverseId` | ✅ |
| By MTGO ID | `GET /cards/mtgo/:id` | `scrython.cards.ByMTGOId` | ✅ |
| By Arena ID | `GET /cards/arena/:id` | `scrython.cards.ByArenaId` | ✅ |
| By TCGPlayer ID | `GET /cards/tcgplayer/:id` | `scrython.cards.ByTCGPlayerId` | ✅ |
| By Cardmarket ID | `GET /cards/cardmarket/:id` | `scrython.cards.ByCardMarketId` | ✅ |
| By Scryfall ID | `GET /cards/:id` | `scrython.cards.ById` | ✅ |

**Endpoints: 13/13 implemented (100%)**

### Card Object Fields

**CoreFieldsMixin (17 properties)**
- All core identifiers: `arena_id`, `id`, `lang`, `mtgo_id`, `mtgo_foil_id`, `multiverse_ids`, `tcgplayer_id`, `tcgplayer_etched_id`, `cardmarket_id`
- Object metadata: `object`, `layout`, `oracle_id`
- API URIs: `prints_search_uri`, `rulings_uri`, `scryfall_uri`, `uri`

**GameplayFieldsMixin (23 properties)**
- All gameplay data: `all_parts`, `card_faces`, `cmc`, `color_identity`, `color_indicator`, `colors`
- Combat stats: `defense`, `power`, `toughness`, `loyalty`
- Rules: `mana_cost`, `oracle_text`, `type_line`, `keywords`, `legalities`
- Modifiers: `hand_modifier`, `life_modifier`
- Rankings: `edhrec_rank`, `penny_rank`
- Special: `produced_mana`, `reserved`

**PrintFieldsMixin (44 properties)**
- Art & flavor: `artist`, `artist_ids`, `flavor_name`, `flavor_text`, `illustration_id`, `watermark`
- Images: `image_uris`, `image_status`, `highres_image`
- Print details: `collector_number`, `rarity`, `border_color`, `frame`, `frame_effects`, `finishes`
- Set info: `set`, `set_name`, `set_type`, `set_uri`, `set_search_uri`, `released_at`
- Prices: `prices`, `purchase_uris`
- Flags: `booster`, `digital`, `foil_only`, `full_art`, `oversized`, `promo`, `reprint`, `textless`, `variation`
- Security: `security_stamp`, `content_warning`
- Preview: `previewed_at`, `preview_source`, `preview_source_uri`
- Special: `attraction_lights`, `games`, `promo_types`

**CardFaceMixin (23 properties)**
- All properties for multi-faced cards (MDFCs, transforms, etc.)

**RelatedCardsObjectMixin (6 properties)**
- Properties for related card objects (tokens, combos, meld pairs)

**Total: 113 card properties with comprehensive type hints** ✅

---

## 2. Sets API ✅ COMPLETE

All 4 set endpoints are fully implemented.

### Endpoints

| Endpoint | Path | Class | Status |
|----------|------|-------|--------|
| All Sets | `GET /sets` | `scrython.sets.All` | ✅ |
| By Code | `GET /sets/:code` | `scrython.sets.ByCode` | ✅ |
| By TCGPlayer ID | `GET /sets/tcgplayer/:id` | `scrython.sets.ByTCGPlayerId` | ✅ |
| By Scryfall ID | `GET /sets/:id` | `scrython.sets.ById` | ✅ |

**Endpoints: 4/4 implemented (100%)**

### Set Object Fields

**SetsObjectMixin (21 properties)**
- Identifiers: `id`, `code`, `mtgo_code`, `arena_code`, `tcgplayer_id`
- Metadata: `object`, `name`, `set_type`, `released_at`
- Structure: `block`, `block_code`, `parent_set_code`
- Counts: `card_count`, `printed_size`
- Flags: `digital`, `foil_only`, `nonfoil_only`
- URIs: `scryfall_uri`, `uri`, `icon_svg_uri`, `search_uri`

**Total: 21 set properties with comprehensive type hints** ✅

---

## 3. Bulk Data API ✅ COMPLETE

All 3 bulk data endpoints are implemented with download functionality.

### Endpoints

| Endpoint | Path | Class | Status |
|----------|------|-------|--------|
| All Bulk Data | `GET /bulk-data` | `scrython.bulk_data.All` | ✅ |
| By ID | `GET /bulk-data/:id` | `scrython.bulk_data.ById` | ✅ |
| By Type | `GET /bulk-data/:type` | `scrython.bulk_data.ByType` | ✅ |

**Endpoints: 3/3 implemented (100%)**

### Bulk Data Object Fields

**BulkDataObjectMixin (11 properties)**
- Identifiers: `id`, `object`, `type`
- Metadata: `name`, `description`, `updated_at`
- Download: `download_uri`, `size`, `content_type`, `content_encoding`
- API: `uri`

**Special Features:**
- ✅ **`download()` method** - Downloads and decompresses bulk data files
  - Automatic gzip decompression
  - Optional file saving with `filepath` parameter
  - Optional progress bar with `progress=True` (requires `pip install scrython[progress]`)
  - Memory-efficient mode with `return_data=False`

**Total: 11 bulk data properties + download functionality** ✅

---

## 4. Rulings API ❌ NOT IMPLEMENTED

**Priority: HIGH** - Commonly used for competitive play and rules questions

### Missing Endpoints

- [ ] `GET /cards/:id/rulings`
- [ ] `GET /cards/multiverse/:id/rulings`
- [ ] `GET /cards/mtgo/:id/rulings`
- [ ] `GET /cards/arena/:id/rulings`
- [ ] `GET /cards/:code/:number/rulings`

**Endpoints: 0/5 implemented (0%)**

### Ruling Object Fields (Not Implemented)

- `object` - Always "ruling"
- `oracle_id` - Associated card's Oracle ID
- `source` - Either "wotc" or "scryfall"
- `published_at` - Ruling publication date
- `comment` - The ruling text

**Implementation Notes:**
- Would need new `scrython.rulings` module
- RulingsMixin for accessing ruling properties
- List mixin support for multiple rulings per card

---

## 5. Symbology API ❌ NOT IMPLEMENTED

**Priority: MEDIUM** - Useful for mana cost parsing and validation

### Missing Endpoints

- [ ] `GET /symbology`
- [ ] `GET /symbology/parse-mana`

**Endpoints: 0/2 implemented (0%)**

### Card Symbol Object Fields (Not Implemented)

14 properties including:
- `symbol`, `loose_variant`, `english`
- `represents_mana`, `mana_value`, `colors`
- `hybrid`, `phyrexian`, `transposable`
- `svg_uri`, `gatherer_alternates`

**Implementation Notes:**
- Would need new `scrython.symbology` module
- Useful for custom card rendering and mana cost validation

---

## 6. Catalogs API ⚠️ PARTIAL IMPLEMENTATION

**Priority: MEDIUM** - Useful for autocomplete, validation, and deckbuilding tools

**Status:** Catalog mixin exists (`ScryfallCatalogMixin`) and is used by `scrython.cards.Autocomplete`

### Missing Endpoints

- [ ] `GET /catalog/card-names`
- [ ] `GET /catalog/artist-names`
- [ ] `GET /catalog/word-bank`
- [ ] `GET /catalog/supertypes`
- [ ] `GET /catalog/card-types`
- [ ] `GET /catalog/artifact-types`
- [ ] `GET /catalog/battle-types`
- [ ] `GET /catalog/creature-types`
- [ ] `GET /catalog/enchantment-types`
- [ ] `GET /catalog/land-types`
- [ ] `GET /catalog/planeswalker-types`
- [ ] `GET /catalog/spell-types`
- [ ] `GET /catalog/powers`
- [ ] `GET /catalog/toughnesses`
- [ ] `GET /catalog/loyalties`
- [ ] `GET /catalog/watermarks`
- [ ] `GET /catalog/keyword-abilities`
- [ ] `GET /catalog/keyword-actions`
- [ ] `GET /catalog/ability-words`
- [ ] `GET /catalog/flavor-words`

**Endpoints: 0/20 implemented (0%)** - though infrastructure exists

### Catalog Object Fields (Already Implemented)

**ScryfallCatalogMixin (4 properties)** ✅
- `object` - Always "catalog"
- `uri` - Link to catalog on API
- `total_values` - Count of items
- `data` - Array of strings

**Implementation Notes:**
- Infrastructure exists, just need endpoint classes
- Would be very easy to implement (simple GET requests)

---

## 7. Card Migrations API ❌ NOT IMPLEMENTED

**Priority: LOW** - Specialized use case for tracking card ID changes

### Missing Endpoints

- [ ] `GET /migrations`
- [ ] `GET /migrations/:id`

**Endpoints: 0/2 implemented (0%)**

### Migration Object Fields (Not Implemented)

9 properties including:
- `object`, `id`, `uri`
- `performed_at`, `migration_strategy`
- `old_scryfall_id`, `new_scryfall_id`
- `note`, `metadata`

**Implementation Notes:**
- Would need new `scrython.migrations` module
- Useful for applications that cache card IDs
- Tracks when Scryfall merges or updates card entries

---

## Testing Coverage

All implemented endpoints have comprehensive test coverage:

✅ **188 total tests passing**
- `test_base.py`: 23 tests (request handling, errors, read-only data)
- `test_bulk_data.py`: 15 tests (endpoints + download functionality)
- `test_cards.py`: 22 tests (all 13 endpoints + mixins)
- `test_sets.py`: 11 tests (all 4 endpoints + mixins)
- `test_property_types.py`: 113 tests (comprehensive property type validation)

**Test Features:**
- Unit tests for all endpoint classes
- Integration tests with mock API responses
- Comprehensive property type testing (113 parametrized tests)
- Error handling tests for invalid requests
- Fixture-based testing with realistic Scryfall responses
- Nullable field handling validation
- Nested object handling (card faces, related cards)

**Code Quality:**
- ✅ All tests passing (188/188)
- ✅ Ruff linting passing
- ✅ Mypy type checking passing
- ✅ Pre-commit hooks configured
- ✅ Comprehensive type hints (Python 3.10+ syntax)

---

## Recent Improvements (Rewrite Branch)

### Phase 1-6 Completed ✅

1. **Factory Pattern Removed** - Direct imports now required
2. **Read-only scryfall_data** - Returns SimpleNamespace with dot-notation access
3. **Comprehensive Type Hints** - Modern Python 3.10+ syntax throughout
4. **Nullable Property Bug Fixed** - All nullable properties use `.get()` method
5. **Bulk Data Download** - Built-in `download()` method with progress bar support
6. **Property Type Testing** - 113 parametrized tests validate all properties
7. **Development Tooling** - black, ruff, mypy, pre-commit hooks

### Bug Fixes

- ✅ Fixed nullable properties raising KeyError when missing from API
- ✅ Fixed `to_object_array` utility to handle missing keys
- ✅ All property type mismatches corrected
- ✅ Test fixtures updated with required fields

---

## Future Roadmap

### Short Term (Next Minor Release)
- Implement Rulings endpoints (high priority)
- Add basic catalog endpoints (card-names, creature-types)
- Improve error messages with more context

### Medium Term
- Implement Symbology endpoints
- Add remaining catalog endpoints
- Consider async/await support for concurrent requests
- Built-in caching layer with TTL

### Long Term
- Complete API coverage (all 49 endpoints)
- Retry logic with exponential backoff
- GraphQL support if Scryfall adds it
- Performance optimizations

---

## Contributing

Want to help implement missing endpoints? See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

New endpoints should follow the established patterns:
1. Create endpoint class inheriting from `ScrythonRequestHandler`
2. Add appropriate mixins for property access
3. Write comprehensive tests with fixtures
4. Update this checklist
5. Add usage examples to README.md

---

**Note:** This document reflects the state of the `rewrite` branch. Some information may differ from the `main` branch.
