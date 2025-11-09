# Scryfall API Implementation Checklist

This document tracks every endpoint and every data point from the Scryfall API, showing what's implemented in Scrython 2.0.

**Legend:**
- ✅ Fully implemented
- ⚠️ Partially implemented (has bugs or missing fields)
- ❌ Not implemented
- 🔧 Endpoint exists but has issues

---

## 1. Cards API

### Endpoints

| Endpoint | Path | Class | Status |
|----------|------|-------|--------|
| Search Cards | `GET /cards/search` | `CardsSearch` | ✅ |
| Named Card Lookup | `GET /cards/named` | `CardsNamed` | ✅ |
| Card Autocomplete | `GET /cards/autocomplete` | `CardsAutocomplete` | ✅ |
| Random Card | `GET /cards/random` | `CardsRandom` | ✅ |
| Card Collection | `POST /cards/collection` | `CardsCollection` | ✅ |
| By Set Code & Number | `GET /cards/:code/:number(/:lang)` | `CardsByCodeNumber` | ✅ |
| By Multiverse ID | `GET /cards/multiverse/:id` | `CardsByMultiverseId` | ✅ |
| By MTGO ID | `GET /cards/mtgo/:id` | `CardsByMTGOId` | ✅ |
| By Arena ID | `GET /cards/arena/:id` | `CardsByArenaId` | ✅ |
| By TCGPlayer ID | `GET /cards/tcgplayer/:id` | `CardsByTCGPlayerId` | ✅ |
| By Cardmarket ID | `GET /cards/cardmarket/:id` | `CardsByCardMarketId` | ✅ |
| By Scryfall ID | `GET /cards/:id` | `CardsById` | ✅ |

**Total: 12/12 endpoints implemented**

---

### Card Object Fields (Core)

| Field | Mixin | Property Name | Status |
|-------|-------|---------------|--------|
| `arena_id` | CoreFieldsMixin | `arena_id` | ✅ |
| `id` | CoreFieldsMixin | `id` | ✅ |
| `lang` | CoreFieldsMixin | `lang` | ✅ |
| `mtgo_id` | CoreFieldsMixin | `mtgo_id` | ✅ |
| `mtgo_foil_id` | CoreFieldsMixin | `mtgo_foil_id` | ✅ |
| `multiverse_ids` | CoreFieldsMixin | `multiverse_ids` | ✅ |
| `resource_id` | — | — | ❌ |
| `tcgplayer_id` | CoreFieldsMixin | `tcgplayer_id` | ✅ |
| `tcgplayer_etched_id` | CoreFieldsMixin | `tcgplayer_etched_id` | ✅ |
| `cardmarket_id` | CoreFieldsMixin | `cardmarket_id` | ✅ |
| `object` | CoreFieldsMixin | `object` | ✅ |
| `layout` | CoreFieldsMixin | `layout` | ✅ |
| `oracle_id` | CoreFieldsMixin | `oracle_id` | ✅ |
| `prints_search_uri` | CoreFieldsMixin | `prints_search_uri` | ✅ |
| `rulings_uri` | CoreFieldsMixin | `rulings_uri` | ✅ |
| `scryfall_uri` | CoreFieldsMixin | `scryfall_uri` | ✅ |
| `uri` | CoreFieldsMixin | `uri` | ✅ |

**Core Fields: 16/17 implemented** (missing: `resource_id`)

---

### Card Object Fields (Gameplay)

| Field | Mixin | Property Name | Status |
|-------|-------|---------------|--------|
| `all_parts` | GameplayFieldsMixin | `all_parts` | ✅ |
| `card_faces` | GameplayFieldsMixin | `card_faces` | ✅ |
| `cmc` | GameplayFieldsMixin | `cmc` | ✅ |
| `color_identity` | GameplayFieldsMixin | `color_identity` | ✅ |
| `color_indicator` | GameplayFieldsMixin | `color_indicator` | ✅ |
| `colors` | GameplayFieldsMixin | `colors` | ✅ |
| `defense` | GameplayFieldsMixin | `defense` | ✅ |
| `edhrec_rank` | GameplayFieldsMixin | `edhrec_rank` | ✅ |
| `game_changer` | GameplayFieldsMixin | `game_changer` | ✅ |
| `hand_modifier` | GameplayFieldsMixin | `hand_modifier` | ✅ |
| `keywords` | GameplayFieldsMixin | `keywords` | ✅ |
| `legalities` | GameplayFieldsMixin | `legalities` | ✅ |
| `life_modifier` | GameplayFieldsMixin | `life_modifier` | ✅ |
| `loyalty` | GameplayFieldsMixin | `loyalty` | ✅ |
| `mana_cost` | GameplayFieldsMixin | `mana_costmissing` | 🔧 **TYPO BUG** |
| `name` | GameplayFieldsMixin | `name` | ✅ |
| `oracle_text` | GameplayFieldsMixin | `oracle_text` | ✅ |
| `penny_rank` | GameplayFieldsMixin | `penny_rank` | ✅ |
| `power` | GameplayFieldsMixin | `power` | ✅ |
| `produced_mana` | GameplayFieldsMixin | `produced_mana` | ✅ |
| `reserved` | GameplayFieldsMixin | `reserved` | ✅ |
| `toughness` | GameplayFieldsMixin | `toughness` | ✅ |
| `type_line` | GameplayFieldsMixin | `type_line` | ✅ |

**Gameplay Fields: 22/23 correct** (1 typo: `mana_costmissing`)

---

### Card Object Fields (Print)

| Field | Mixin | Property Name | Status |
|-------|-------|---------------|--------|
| `artist` | PrintFieldsMixin | `artist` | ✅ |
| `artist_ids` | PrintFieldsMixin | `artist_ids` | ✅ |
| `attraction_lights` | PrintFieldsMixin | `attraction_lights` | ✅ |
| `booster` | PrintFieldsMixin | `booster` | ✅ |
| `border_color` | PrintFieldsMixin | `border_color` | ✅ |
| `card_back_id` | PrintFieldsMixin | `card_back_id` | ✅ |
| `collector_number` | PrintFieldsMixin | `collector_number` | ✅ |
| `content_warning` | PrintFieldsMixin | `content_warning` | ✅ |
| `digital` | PrintFieldsMixin | `digital` | ✅ |
| `finishes` | PrintFieldsMixin | `finishes` | ✅ |
| `flavor_name` | PrintFieldsMixin | `flavor_name` | ✅ |
| `flavor_text` | PrintFieldsMixin | `flavor_text` | ✅ |
| `frame_effects` | PrintFieldsMixin | `frame_effects` | ✅ |
| `frame` | PrintFieldsMixin | `frame` | ✅ |
| `full_art` | PrintFieldsMixin | `full_art` | ✅ |
| `games` | PrintFieldsMixin | `games` | ✅ |
| `highres_image` | PrintFieldsMixin | `highres_image` | ✅ |
| `illustration_id` | PrintFieldsMixin | `illustration_idfield` | 🔧 **TYPO BUG** |
| `image_status` | PrintFieldsMixin | `image_status` | ✅ |
| `image_uris` | PrintFieldsMixin | `image_uris` | ✅ |
| `oversized` | PrintFieldsMixin | `oversized` | ✅ |
| `prices` | PrintFieldsMixin | `pricesas` | 🔧 **TYPO BUG** |
| `printed_name` | PrintFieldsMixin | `printed_name` | ✅ |
| `printed_text` | PrintFieldsMixin | `printed_text` | ✅ |
| `printed_type_line` | PrintFieldsMixin | `printed_type_line` | ✅ |
| `promo` | PrintFieldsMixin | `promo` | ✅ |
| `promo_types` | PrintFieldsMixin | `promo_types` | ✅ |
| `purchase_uris` | PrintFieldsMixin | `purchase_uris` | ✅ |
| `rarity` | PrintFieldsMixin | `rarity` | ✅ |
| `related_uris` | PrintFieldsMixin | `related_uris` | ✅ |
| `released_at` | PrintFieldsMixin | `released_at` | ✅ |
| `reprint` | PrintFieldsMixin | `reprint` | ✅ |
| `scryfall_set_uri` | PrintFieldsMixin | `scryfall_set_uri` | ✅ |
| `set_name` | PrintFieldsMixin | `set_name` | ✅ |
| `set_search_uri` | PrintFieldsMixin | `set_search_uri` | ✅ |
| `set_type` | PrintFieldsMixin | `set_type` | ✅ |
| `set_uri` | PrintFieldsMixin | `set_uri` | ✅ |
| `set` | PrintFieldsMixin | `set` | ✅ |
| `set_id` | PrintFieldsMixin | `set_id` | ✅ |
| `story_spotlight` | PrintFieldsMixin | `story_spotlight` | ✅ |
| `textless` | PrintFieldsMixin | `textless` | ✅ |
| `variation` | PrintFieldsMixin | `variation` | ✅ |
| `variation_of` | PrintFieldsMixin | `variation_of` | ✅ |
| `security_stamp` | PrintFieldsMixin | `security_stamp` | ✅ |
| `watermark` | PrintFieldsMixin | `watermark` | ✅ |
| `preview.previewed_at` | PrintFieldsMixin | `previewed_at` | ✅ |
| `preview.source_uri` | PrintFieldsMixin | `preview_source_uri` | ✅ |
| `preview.source` | PrintFieldsMixin | `preview_source` | ✅ |

**Print Fields: 46/48 correct** (2 typos: `illustration_idfield`, `pricesas`)

---

### Card Face Object Fields

| Field | Mixin | Property Name | Status |
|-------|-------|---------------|--------|
| `artist` | CardFaceMixin | `artist` | ✅ |
| `artist_id` | CardFaceMixin | `artist_id` | ✅ |
| `cmc` | CardFaceMixin | `cmc` | ✅ |
| `color_indicator` | CardFaceMixin | `color_indicator` | ✅ |
| `colors` | CardFaceMixin | `colors` | ✅ |
| `defense` | CardFaceMixin | `defense` | ✅ |
| `flavor_text` | CardFaceMixin | `flavor_text` | ✅ |
| `illustration_id` | CardFaceMixin | `illustration_id` | ✅ |
| `image_uris` | CardFaceMixin | `image_uris` | ✅ |
| `layout` | CardFaceMixin | `layout` | ✅ |
| `loyalty` | CardFaceMixin | `loyalty` | ✅ |
| `mana_cost` | CardFaceMixin | `mana_costmana` | 🔧 **TYPO BUG** |
| `name` | CardFaceMixin | `name` | ✅ |
| `object` | CardFaceMixin | `object` | ✅ |
| `oracle_id` | CardFaceMixin | `oracle_id` | ✅ |
| `oracle_text` | CardFaceMixin | `oracle_text` | ✅ |
| `power` | CardFaceMixin | `power` | ✅ |
| `printed_name` | CardFaceMixin | `printed_name` | ✅ |
| `printed_text` | CardFaceMixin | `printed_text` | ✅ |
| `printed_type_line` | CardFaceMixin | `printed_type_line` | ✅ |
| `toughness` | CardFaceMixin | `toughness` | ✅ |
| `type_line` | CardFaceMixin | `type_line` | ✅ |
| `watermark` | CardFaceMixin | `watermark` | ✅ |

**Card Face Fields: 22/23 correct** (1 typo: `mana_costmana`)

---

### Related Card Object Fields

| Field | Mixin | Property Name | Status |
|-------|-------|---------------|--------|
| `id` | RelatedCardsObjectMixin | `id` | ✅ |
| `object` | RelatedCardsObjectMixin | `object` | ✅ |
| `component` | RelatedCardsObjectMixin | `component` | ✅ |
| `name` | RelatedCardsObjectMixin | `name` | ✅ |
| `type_line` | RelatedCardsObjectMixin | `type_line` | ✅ |
| `uri` | RelatedCardsObjectMixin | `uri` | ✅ |

**Related Card Fields: 6/6 implemented** ✅

---

## 2. Sets API

### Endpoints

| Endpoint | Path | Class | Status |
|----------|------|-------|--------|
| All Sets | `GET /sets` | `AllSets` | ✅ |
| By Code | `GET /sets/:code` | `SetsByCode` | ✅ |
| By TCGPlayer ID | `GET /sets/tcgplayer/:id` | `SetsByTCGPlayerId` | ✅ |
| By Scryfall ID | `GET /sets/:id` | `SetsById` | ✅ |

**Total: 4/4 endpoints implemented**

---

### Set Object Fields

| Field | Mixin | Property Name | Status |
|-------|-------|---------------|--------|
| `object` | SetsObjectMixin | `object` | ✅ |
| `id` | SetsObjectMixin | `id` | ✅ |
| `code` | SetsObjectMixin | `code` | ✅ |
| `mtgo_code` | SetsObjectMixin | `mtgo_code` | ✅ |
| `arena_code` | SetsObjectMixin | `arena_code` | ✅ |
| `tcgplayer_id` | SetsObjectMixin | `tcgplayer_id` | ✅ |
| `name` | SetsObjectMixin | `name` | ✅ |
| `set_type` | SetsObjectMixin | `set_type` | ✅ |
| `released_at` | SetsObjectMixin | `released_at` | ✅ |
| `block_code` | SetsObjectMixin | `block_code` | ✅ |
| `block` | SetsObjectMixin | `block` | ✅ |
| `parent_set_code` | SetsObjectMixin | `parent_set_code` | ✅ |
| `card_count` | SetsObjectMixin | `card_count` | ✅ |
| `printed_size` | SetsObjectMixin | `printed_size` | ✅ |
| `digital` | SetsObjectMixin | `digital` | ✅ |
| `foil_only` | SetsObjectMixin | `foil_only` | ✅ |
| `nonfoil_only` | SetsObjectMixin | `nonfoil_only` | ✅ |
| `scryfall_uri` | SetsObjectMixin | `scryfall_uri` | ✅ |
| `uri` | SetsObjectMixin | `uri` | ✅ |
| `icon_svg_uri` | SetsObjectMixin | `icon_svg_uri` | ✅ |
| `search_uri` | SetsObjectMixin | `search_uri` | ✅ |

**Set Fields: 21/21 implemented** ✅

---

## 3. Bulk Data API

### Endpoints

| Endpoint | Path | Class | Status |
|----------|------|-------|--------|
| All Bulk Data | `GET /bulk-data` | `AllBulkData` | ✅ |
| By ID | `GET /bulk-data/:id` | `BulkDataById` | ✅ |
| By Type | `GET /bulk-data/:type` | `BulkDataByType` | ✅ |

**Total: 3/3 endpoints implemented**

---

### Bulk Data Object Fields

| Field | Mixin | Property Name | Status |
|-------|-------|---------------|--------|
| `id` | BulkDataObjectMixin | `id` | ✅ |
| `uri` | BulkDataObjectMixin | `uri` | ✅ |
| `type` | BulkDataObjectMixin | `type` | ✅ |
| `name` | BulkDataObjectMixin | `name` | ✅ |
| `description` | BulkDataObjectMixin | `description` | ✅ |
| `download_uri` | BulkDataObjectMixin | `download_uri` | ✅ |
| `updated_at` | BulkDataObjectMixin | `updated_at` | ✅ |
| `size` | BulkDataObjectMixin | `size` | ✅ |
| `content_type` | BulkDataObjectMixin | `content_type` | ✅ |
| `content_encoding` | BulkDataObjectMixin | `content_encoding` | ✅ |
| `object` | BulkDataObjectMixin | `object` | ✅ |

**Bulk Data Fields: 11/11 implemented** ✅

---

## 4. Rulings API ❌ NOT IMPLEMENTED

### Endpoints

| Endpoint | Path | Class | Status |
|----------|------|-------|--------|
| By Multiverse ID | `GET /cards/multiverse/:id/rulings` | — | ❌ |
| By MTGO ID | `GET /cards/mtgo/:id/rulings` | — | ❌ |
| By Arena ID | `GET /cards/arena/:id/rulings` | — | ❌ |
| By Set Code & Number | `GET /cards/:code/:number/rulings` | — | ❌ |
| By Scryfall ID | `GET /cards/:id/rulings` | — | ❌ |

**Total: 0/5 endpoints implemented**

---

### Ruling Object Fields

| Field | Type | Description | Status |
|-------|------|-------------|--------|
| `object` | String | Always "ruling" | ❌ |
| `oracle_id` | UUID | Associated card's Oracle ID | ❌ |
| `source` | String | Either "wotc" or "scryfall" | ❌ |
| `published_at` | Date | Ruling publication date | ❌ |
| `comment` | String | The ruling text | ❌ |

**Ruling Fields: 0/5 implemented**

---

## 5. Catalogs API ❌ NOT IMPLEMENTED

### Endpoints

| Endpoint | Path | Status |
|----------|------|--------|
| Card Names | `GET /catalog/card-names` | ❌ |
| Artist Names | `GET /catalog/artist-names` | ❌ |
| Word Bank | `GET /catalog/word-bank` | ❌ |
| Supertypes | `GET /catalog/supertypes` | ❌ |
| Card Types | `GET /catalog/card-types` | ❌ |
| Artifact Types | `GET /catalog/artifact-types` | ❌ |
| Battle Types | `GET /catalog/battle-types` | ❌ |
| Creature Types | `GET /catalog/creature-types` | ❌ |
| Enchantment Types | `GET /catalog/enchantment-types` | ❌ |
| Land Types | `GET /catalog/land-types` | ❌ |
| Planeswalker Types | `GET /catalog/planeswalker-types` | ❌ |
| Spell Types | `GET /catalog/spell-types` | ❌ |
| Powers | `GET /catalog/powers` | ❌ |
| Toughnesses | `GET /catalog/toughnesses` | ❌ |
| Loyalties | `GET /catalog/loyalties` | ❌ |
| Keyword Abilities | `GET /catalog/keyword-abilities` | ❌ |
| Keyword Actions | `GET /catalog/keyword-actions` | ❌ |
| Ability Words | `GET /catalog/ability-words` | ❌ |
| Flavor Words | `GET /catalog/flavor-words` | ❌ |
| Watermarks | `GET /catalog/watermarks` | ❌ |

**Total: 0/19 endpoints implemented**

---

### Catalog Object Fields

| Field | Type | Description | Status |
|-------|------|-------------|--------|
| `object` | String | Always "catalog" | ❌ |
| `uri` | URI | Link to catalog on API | ❌ |
| `total_values` | Integer | Count of items | ❌ |
| `data` | Array | Array of strings | ❌ |

**Catalog Fields: 0/4 implemented**

**Note**: `CardsAutocomplete` returns a catalog object, so `ScryfallCatalogMixin` exists with these fields implemented!

---

## 6. Symbology API ❌ NOT IMPLEMENTED

### Endpoints

| Endpoint | Path | Status |
|----------|------|--------|
| All Symbols | `GET /symbology` | ❌ |
| Parse Mana | `GET /symbology/parse-mana` | ❌ |

**Total: 0/2 endpoints implemented**

---

### Card Symbol Object Fields

| Field | Type | Description | Status |
|-------|------|-------------|--------|
| `object` | String | Always "card_symbol" | ❌ |
| `symbol` | String | Plaintext representation | ❌ |
| `loose_variant` | String | Alternate notation | ❌ |
| `english` | String | Human-readable description | ❌ |
| `transposable` | Boolean | Can be written in reverse | ❌ |
| `represents_mana` | Boolean | Is a mana symbol | ❌ |
| `mana_value` | Decimal | CMC value | ❌ |
| `appears_in_mana_costs` | Boolean | Appears in costs | ❌ |
| `funny` | Boolean | From Un-sets | ❌ |
| `colors` | Array | Associated colors | ❌ |
| `hybrid` | Boolean | Hybrid mana | ❌ |
| `phyrexian` | Boolean | Phyrexian mana | ❌ |
| `gatherer_alternates` | String | Legacy notations | ❌ |
| `svg_uri` | URI | SVG graphic link | ❌ |

**Symbol Fields: 0/14 implemented**

---

## 7. Card Migrations API (Beta) ❌ NOT IMPLEMENTED

### Endpoints

| Endpoint | Path | Status |
|----------|------|--------|
| All Migrations | `GET /migrations` | ❌ |
| By ID | `GET /migrations/:id` | ❌ |

**Total: 0/2 endpoints implemented**

---

### Migration Object Fields

| Field | Type | Description | Status |
|-------|------|-------------|--------|
| `object` | String | Always "migration" | ❌ |
| `uri` | URI | API link to migration | ❌ |
| `id` | UUID | Unique identifier | ❌ |
| `performed_at` | Date | Migration timestamp | ❌ |
| `migration_strategy` | String | "merge" or "delete" | ❌ |
| `old_scryfall_id` | UUID | Original card ID | ❌ |
| `new_scryfall_id` | UUID | Replacement ID (nullable) | ❌ |
| `note` | String | Context about migration | ❌ |
| `metadata` | Object | Additional context | ❌ |

**Migration Fields: 0/9 implemented**

---

## Summary Statistics

### Endpoints by Category

| Category | Implemented | Total | Percentage |
|----------|-------------|-------|------------|
| Cards | 12 | 12 | 100% ✅ |
| Sets | 4 | 4 | 100% ✅ |
| Bulk Data | 3 | 3 | 100% ✅ |
| Rulings | 0 | 5 | 0% ❌ |
| Catalogs | 0 | 19 | 0% ❌ |
| Symbology | 0 | 2 | 0% ❌ |
| Migrations | 0 | 2 | 0% ❌ |
| **TOTAL** | **19** | **47** | **40.4%** |

---

### Fields by Category

| Category | Correct | Total | Issues |
|----------|---------|-------|--------|
| Card Core | 16 | 17 | 1 missing (`resource_id`) |
| Card Gameplay | 22 | 23 | 1 typo (`mana_costmissing`) |
| Card Print | 46 | 48 | 2 typos (`illustration_idfield`, `pricesas`) |
| Card Face | 22 | 23 | 1 typo (`mana_costmana`) |
| Related Card | 6 | 6 | 0 ✅ |
| Set | 21 | 21 | 0 ✅ |
| Bulk Data | 11 | 11 | 0 ✅ |
| Ruling | 0 | 5 | Not implemented |
| Catalog | 4 | 4 | Implemented via `ScryfallCatalogMixin` ✅ |
| Symbol | 0 | 14 | Not implemented |
| Migration | 0 | 9 | Not implemented |

---

## Critical Bugs to Fix

### Property Name Typos (cards_mixins.py)

1. **Line 137**: `mana_costmissing` → should be `mana_cost`
2. **Line 242**: `illustration_idfield` → should be `illustration_id`
3. **Line 258**: `pricesas` → should be `prices`
4. **Line 411**: `mana_costmana` → should be `mana_cost`

---

## Missing Implementations (Future Work)

### High Priority
- Rulings API (5 endpoints)
- Basic Catalog endpoints (card-names, artist-names)

### Medium Priority
- Symbology API (2 endpoints)
- Extended Catalog endpoints (types, powers, toughnesses, etc.)

### Low Priority
- Card Migrations API (2 endpoints, beta feature)

---

## Notes

1. **Catalog Mixin**: The `ScryfallCatalogMixin` exists and is used by `CardsAutocomplete`, so catalog functionality is partially supported
2. **Bulk Data**: Need to verify `bulk_data_mixins.py` for complete field list
3. **Missing Field**: `resource_id` is not implemented in Card objects (low priority, rarely used)
4. **Factory Pattern**: All implemented endpoints use the smart factory pattern correctly
