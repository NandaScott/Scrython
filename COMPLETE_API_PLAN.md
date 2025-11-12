# Comprehensive Plan: Complete Scryfall API Implementation

**Current Status:** 49/49 endpoints (100% coverage) ✅ **COMPLETE!**
- Cards API: ✅ 13/13 endpoints (100%)
- Sets API: ✅ 4/4 endpoints (100%)
- Bulk Data API: ✅ 3/3 endpoints (100%)
- Rulings API: ✅ 5/5 endpoints (100%) **NEW!**
- Symbology API: ✅ 2/2 endpoints (100%) **NEW!**
- Catalogs API: ✅ 20/20 endpoints (100%) **NEW!**
- Migrations API: ✅ 2/2 endpoints (100%) **NEW!**

**Goal:** ✅ **ACHIEVED** - All 49 Scryfall API endpoints implemented!

---

## Phase 1: Rulings API (HIGH PRIORITY)

**Endpoints:** 5 endpoints (0% → 100%)
**Estimated Time:** 3-4 hours
**Priority:** HIGH - Most requested feature for competitive play and rules questions

### Endpoints to Implement

| Endpoint | Path | Description |
|----------|------|-------------|
| RulingsById | GET /cards/:id/rulings | Get rulings for a card by Scryfall UUID |
| RulingsByMultiverseId | GET /cards/multiverse/:id/rulings | Get rulings by Multiverse ID |
| RulingsByMTGOId | GET /cards/mtgo/:id/rulings | Get rulings by MTGO ID |
| RulingsByArenaId | GET /cards/arena/:id/rulings | Get rulings by Arena ID |
| RulingsByCodeNumber | GET /cards/:code/:number/rulings | Get rulings by set code and collector number |

### Ruling Object Properties

All rulings return a list of Ruling objects with these properties:
- `object` - Always "ruling"
- `oracle_id` - UUID for the card's oracle identity
- `source` - Either "wotc" or "scryfall"
- `published_at` - Publication date (ISO 8601 format)
- `comment` - The ruling text

### Implementation Steps

1. **Create module structure:**
   ```
   scrython/rulings/
   ├── __init__.py          # Export Rulings factory and endpoint classes
   ├── rulings.py           # 5 endpoint classes + Rulings factory
   └── rulings_mixins.py    # RulingsObjectMixin with 5 properties
   ```

2. **Implement RulingsObjectMixin:**
   - Add `@property` accessors for all 5 ruling fields
   - Use `.get()` for nullable fields
   - Include type hints and docstrings

3. **Implement 5 endpoint classes:**
   - Each inherits from `ScrythonRequestHandler` + `ScryfallListMixin` + `RulingsObjectMixin`
   - Set `_endpoint` class variable with appropriate path template
   - Use `:id`, `:code`, `:number` path parameters as needed
   - All return list responses (multiple rulings per card)

4. **Create Rulings smart factory:**
   ```python
   class Rulings:
       def __new__(cls, **kwargs):
           if 'id' in kwargs:
               return RulingsById(**kwargs)
           elif 'multiverse_id' in kwargs:
               return RulingsByMultiverseId(**kwargs)
           elif 'mtgo_id' in kwargs:
               return RulingsByMTGOId(**kwargs)
           elif 'arena_id' in kwargs:
               return RulingsByArenaId(**kwargs)
           elif 'code' in kwargs and 'number' in kwargs:
               return RulingsByCodeNumber(**kwargs)
           else:
               raise ValueError("Invalid parameters for Rulings")
   ```

5. **Write comprehensive tests:**
   - Create fixtures for ruling responses
   - Test all 5 endpoint classes
   - Test property access
   - Test error handling
   - Test list navigation

6. **Update main `__init__.py`:**
   - Add `from scrython.rulings import Rulings`
   - Export in `__all__`

### Example Usage After Implementation

```python
import scrython

# Get rulings by card ID
rulings = scrython.Rulings(id="f2b9983e-20d4-4d12-9e2c-ec6d9a345787")
for ruling in rulings.data():
    print(f"{ruling.published_at}: {ruling.comment}")

# Get rulings by set code and number
rulings = scrython.Rulings(code="m21", number="241")
print(f"Found {rulings.total_values()} rulings")
```

---

## Phase 2: Core Catalogs API (MEDIUM PRIORITY - Part 1)

**Endpoints:** 10 most useful catalogs (0% → 50%)
**Estimated Time:** 2-3 hours
**Priority:** MEDIUM - Enables input validation and autocomplete features

### Endpoints to Implement (High-Value Catalogs)

| Endpoint | Path | Use Case |
|----------|------|----------|
| CardNames | GET /catalog/card-names | Autocomplete, validation |
| CreatureTypes | GET /catalog/creature-types | Tribal deckbuilding, validation |
| PlaneswalkerTypes | GET /catalog/planeswalker-types | Card validation |
| CardTypes | GET /catalog/card-types | Type validation |
| KeywordAbilities | GET /catalog/keyword-abilities | Rules reference, parsing |
| KeywordActions | GET /catalog/keyword-actions | Rules reference |
| ArtifactTypes | GET /catalog/artifact-types | Card validation |
| EnchantmentTypes | GET /catalog/enchantment-types | Card validation |
| LandTypes | GET /catalog/land-types | Mana base validation |
| SpellTypes | GET /catalog/spell-types | Card validation |

### Catalog Object Structure

All catalogs return the same structure (already supported via `ScryfallCatalogMixin`):
- `object` - Always "catalog"
- `uri` - API link to this catalog
- `total_values` - Count of items in the array
- `data` - Array of strings

### Implementation Steps

1. **Create module structure:**
   ```
   scrython/catalogs/
   ├── __init__.py          # Export Catalogs factory
   └── catalogs.py          # All catalog endpoint classes
   ```

2. **Implement 10 endpoint classes:**
   - Each inherits from `ScrythonRequestHandler` + `ScryfallCatalogMixin`
   - Set `_endpoint` class variable (e.g., `/catalog/card-names`)
   - No custom properties needed - `ScryfallCatalogMixin` handles everything

3. **Create Catalogs smart factory:**
   ```python
   class Catalogs:
       def __new__(cls, catalog_type: str, **kwargs):
           catalog_map = {
               'card-names': CardNames,
               'creature-types': CreatureTypes,
               'planeswalker-types': PlaneswalkerTypes,
               # ... etc
           }
           if catalog_type in catalog_map:
               return catalog_map[catalog_type](**kwargs)
           else:
               raise ValueError(f"Unknown catalog type: {catalog_type}")
   ```

4. **Write tests:**
   - Create fixtures for each catalog type
   - Test catalog data access
   - Verify `total_values` and `data()` methods
   - Test factory routing

5. **Update main `__init__.py`**

### Example Usage After Implementation

```python
import scrython

# Get all creature types
creatures = scrython.Catalogs('creature-types')
print(f"Total creature types: {creatures.total_values()}")
print("Some tribes:", creatures.data()[:10])

# Get all keyword abilities
keywords = scrython.Catalogs('keyword-abilities')
if "Flying" in keywords.data():
    print("Flying is a keyword ability")
```

---

## Phase 3: Symbology API (MEDIUM PRIORITY)

**Endpoints:** 2 endpoints (0% → 100%)
**Estimated Time:** 2-3 hours
**Priority:** MEDIUM - Useful for mana cost parsing and custom rendering

### Endpoints to Implement

| Endpoint | Path | Description |
|----------|------|-------------|
| SymbologyAll | GET /symbology | Retrieve all card symbols in the system |
| SymbologyParseMana | GET /symbology/parse-mana | Parse mana cost notation into structured data |

### Card Symbol Object Properties (14 total)

- `object` - Always "card_symbol"
- `symbol` - The raw text symbol (e.g., "{W}", "{U/B}")
- `loose_variant` - Alternate symbol for loose searches
- `english` - English description
- `transposable` - Can be replaced with other symbols (Boolean)
- `represents_mana` - Whether this symbol represents mana (Boolean)
- `mana_value` - Numeric mana value (can be fractional)
- `appears_in_mana_costs` - Appears in mana costs (Boolean)
- `funny` - Appears on funny cards only (Boolean)
- `colors` - Array of color abbreviations
- `hybrid` - Is hybrid mana symbol (Boolean)
- `phyrexian` - Is Phyrexian mana symbol (Boolean)
- `cmc` - Converted mana cost contribution (deprecated, use mana_value)
- `svg_uri` - SVG image URI
- `gatherer_alternates` - Array of alternative Gatherer representations

### ParseMana Response Object

The parse-mana endpoint returns a ManaCost object:
- `object` - Always "mana_cost"
- `cost` - The original mana cost string
- `cmc` - Total converted mana cost (deprecated)
- `mana_value` - Total mana value
- `colors` - Array of colors in the cost
- `colorless` - Whether the cost is colorless (Boolean)
- `monocolored` - Whether the cost is monocolored (Boolean)
- `multicolored` - Whether the cost is multicolored (Boolean)

### Implementation Steps

1. **Create module structure:**
   ```
   scrython/symbology/
   ├── __init__.py              # Export Symbology factory
   ├── symbology.py             # 2 endpoint classes
   └── symbology_mixins.py      # SymbologyObjectMixin + ManaCostMixin
   ```

2. **Implement SymbologyObjectMixin:**
   - Add `@property` accessors for all 14 symbol fields
   - Include type hints (Boolean fields, arrays, etc.)
   - Comprehensive docstrings

3. **Implement ManaCostMixin:**
   - Add `@property` accessors for ParseMana response fields
   - Handle the unique response structure

4. **Implement endpoint classes:**
   - `SymbologyAll` - Inherits from `ScrythonRequestHandler` + `ScryfallListMixin` + `SymbologyObjectMixin`
   - `SymbologyParseMana` - Inherits from `ScrythonRequestHandler` + `ManaCostMixin`
   - ParseMana takes `cost` parameter (e.g., `cost="{2}{U}{U}"`)

5. **Create Symbology smart factory:**
   ```python
   class Symbology:
       def __new__(cls, **kwargs):
           if 'cost' in kwargs:
               return SymbologyParseMana(**kwargs)
           else:
               return SymbologyAll(**kwargs)
   ```

6. **Write comprehensive tests:**
   - Test symbol list retrieval
   - Test mana cost parsing with various costs
   - Test property access
   - Test color detection

7. **Update main `__init__.py`**

### Example Usage After Implementation

```python
import scrython

# Get all symbols
symbols = scrython.Symbology()
for symbol in symbols.data():
    if symbol.represents_mana:
        print(f"{symbol.symbol}: {symbol.english}")

# Parse a mana cost
cost = scrython.Symbology(cost="{2}{U}{U}")
print(f"Mana value: {cost.mana_value()}")  # 4
print(f"Colors: {cost.colors()}")  # ['U']
print(f"Monocolored: {cost.monocolored()}")  # True
```

---

## Phase 4: Complete Catalogs API (MEDIUM PRIORITY - Part 2)

**Endpoints:** 10 remaining catalogs (50% → 100%)
**Estimated Time:** 2 hours
**Priority:** MEDIUM - Complete catalog coverage

### Endpoints to Implement (Remaining Catalogs)

| Endpoint | Path | Use Case |
|----------|------|----------|
| ArtistNames | GET /catalog/artist-names | Artist search, attribution |
| WordBank | GET /catalog/word-bank | Card text search |
| Supertypes | GET /catalog/supertypes | Type validation (Legendary, Basic, etc.) |
| BattleTypes | GET /catalog/battle-types | Battle card validation |
| Powers | GET /catalog/powers | Creature stat validation |
| Toughnesses | GET /catalog/toughnesses | Creature stat validation |
| Loyalties | GET /catalog/loyalties | Planeswalker validation |
| Watermarks | GET /catalog/watermarks | Card identification |
| AbilityWords | GET /catalog/ability-words | Card text parsing |
| FlavorWords | GET /catalog/flavor-words | Flavor text reference |

### Implementation Steps

1. **Add 10 endpoint classes to `catalogs.py`:**
   - Same pattern as Phase 2
   - Each inherits from `ScrythonRequestHandler` + `ScryfallCatalogMixin`
   - Simple `_endpoint` class variable

2. **Update Catalogs factory:**
   - Add all 10 new catalog types to the routing map
   - Now supports all 20 catalog endpoints

3. **Extend test coverage:**
   - Add fixtures for new catalog types
   - Test factory routing for all 20 types

4. **Complete catalog documentation:**
   - Document all 20 catalog types with examples

### Example Usage After Implementation

```python
import scrython

# Get all artist names
artists = scrython.Catalogs('artist-names')
if "Rebecca Guay" in artists.data():
    print("Rebecca Guay has illustrated cards")

# Get all possible power values
powers = scrython.Catalogs('powers')
print("Possible power values:", powers.data())

# Get watermarks
watermarks = scrython.Catalogs('watermarks')
print(f"Total watermarks: {watermarks.total_values()}")
```

---

## Phase 5: Migrations API (LOW PRIORITY)

**Endpoints:** 2 endpoints (0% → 100%)
**Estimated Time:** 2-3 hours
**Priority:** LOW - Specialized use case for applications that cache data

### Endpoints to Implement

| Endpoint | Path | Description |
|----------|------|-------------|
| MigrationsAll | GET /migrations | Retrieve recent migrations (with pagination) |
| MigrationsById | GET /migrations/:id | Access a specific migration record by UUID |

### Migration Object Properties (9 total)

- `object` - Always "migration"
- `id` - Migration UUID
- `uri` - API URI for this migration
- `performed_at` - Timestamp of migration (ISO 8601)
- `migration_strategy` - Either "merge" or "delete"
- `old_scryfall_id` - Original card UUID
- `new_scryfall_id` - Replacement UUID (nullable - null if deleted)
- `note` - Optional explanation from Scryfall team (nullable)
- `metadata` - Additional context data (object)

### Use Cases

- Applications that cache card data locally need to reconcile ID changes
- Tracking when Scryfall removes duplicate card entries
- Syncing local databases with upstream Scryfall changes
- Understanding historical card database evolution

### Implementation Steps

1. **Create module structure:**
   ```
   scrython/migrations/
   ├── __init__.py              # Export Migrations factory
   ├── migrations.py            # 2 endpoint classes
   └── migrations_mixins.py     # MigrationsObjectMixin with 9 properties
   ```

2. **Implement MigrationsObjectMixin:**
   - Add `@property` accessors for all 9 fields
   - Use `.get()` for nullable fields (new_scryfall_id, note)
   - Include type hints and docstrings

3. **Implement endpoint classes:**
   - `MigrationsAll` - Inherits from `ScrythonRequestHandler` + `ScryfallListMixin` + `MigrationsObjectMixin`
     - Supports pagination (has_more, next_page, etc.)
   - `MigrationsById` - Inherits from `ScrythonRequestHandler` + `MigrationsObjectMixin`
     - Simple ID lookup

4. **Create Migrations smart factory:**
   ```python
   class Migrations:
       def __new__(cls, **kwargs):
           if 'id' in kwargs:
               return MigrationsById(**kwargs)
           else:
               return MigrationsAll(**kwargs)
   ```

5. **Write tests:**
   - Create fixtures for migration responses
   - Test both merge and delete strategies
   - Test pagination for MigrationsAll
   - Test nullable field handling

6. **Update main `__init__.py`**

### Example Usage After Implementation

```python
import scrython

# Get recent migrations
migrations = scrython.Migrations()
for migration in migrations.data():
    if migration.migration_strategy() == "merge":
        print(f"Card {migration.old_scryfall_id()} merged into {migration.new_scryfall_id()}")
    else:
        print(f"Card {migration.old_scryfall_id()} was deleted")

# Get a specific migration by ID
migration = scrython.Migrations(id="12345678-1234-1234-1234-123456789012")
print(f"Migration performed at: {migration.performed_at()}")
if migration.note():
    print(f"Note: {migration.note()}")
```

---

## Phase 6: Integration & Polish

**Estimated Time:** 2-3 hours

### Tasks

1. **Run full test suite:**
   - All 188+ existing tests must still pass
   - All new tests must pass
   - Aim for 100% code coverage on new modules

2. **Update IMPLEMENTATION_PLAN.md:**
   - Mark all phases as complete
   - Update status to "100% API Coverage Achieved"
   - Document the completion date

3. **Update README.md:**
   - Add examples for all new API modules
   - Update feature list
   - Add coverage statistics (49/49 endpoints)

4. **Create comprehensive examples:**
   - `examples/rulings_examples.py` - Common ruling queries
   - `examples/symbology_examples.py` - Mana cost parsing
   - `examples/catalogs_examples.py` - Validation use cases
   - `examples/migrations_examples.py` - Database sync patterns

5. **Verify type hints:**
   - Run `mypy` on all new code
   - Ensure no type errors
   - Add missing type hints if needed

6. **Final code review:**
   - Check consistency with existing codebase style
   - Verify all docstrings are comprehensive
   - Ensure error handling is consistent
   - Check that all nullable fields use `.get()`

7. **Performance testing:**
   - Test rate limit guidance (reminder: library doesn't enforce limits)
   - Verify memory efficiency with large catalog responses
   - Test pagination performance

8. **Documentation:**
   - Update API reference documentation
   - Add migration guide for users
   - Document any breaking changes (if any)

---

## Implementation Summary

### Total Effort Estimate
**11-17 hours** to achieve 100% Scryfall API coverage

### Effort Breakdown by Phase
- Phase 1 (Rulings): 3-4 hours
- Phase 2 (Core Catalogs): 2-3 hours
- Phase 3 (Symbology): 2-3 hours
- Phase 4 (Remaining Catalogs): 2 hours
- Phase 5 (Migrations): 2-3 hours
- Phase 6 (Integration & Polish): 2-3 hours

### Final Coverage
- **Cards API:** 13/13 endpoints ✅
- **Sets API:** 4/4 endpoints ✅
- **Bulk Data API:** 3/3 endpoints ✅
- **Rulings API:** 5/5 endpoints ✅ (NEW)
- **Symbology API:** 2/2 endpoints ✅ (NEW)
- **Catalogs API:** 20/20 endpoints ✅ (NEW)
- **Migrations API:** 2/2 endpoints ✅ (NEW)

**TOTAL: 49/49 endpoints (100% coverage)** 🎉

---

## Success Criteria

Before marking complete, verify:

- ✅ All 49 Scryfall API endpoints implemented
- ✅ 100% test coverage for new endpoints (all tests passing)
- ✅ Comprehensive docstrings with examples on all classes and properties
- ✅ Type hints on all new code (mypy clean)
- ✅ Consistent architecture with existing codebase patterns
- ✅ Updated documentation (README.md, IMPLEMENTATION_PLAN.md)
- ✅ Working examples for each new module
- ✅ No regression in existing functionality
- ✅ Code style matches Contributing.md guidelines
- ✅ All nullable fields properly handled with `.get()`
- ✅ All error cases tested
- ✅ Pagination tested for list endpoints

---

## Architecture Notes

All new implementations should follow these patterns from the existing codebase:

### Module Structure Pattern
```
scrython/{module_name}/
├── __init__.py              # Exports
├── {module_name}.py         # Endpoint classes + Factory
└── {module_name}_mixins.py  # Property accessors
```

### Endpoint Class Pattern
```python
class EndpointName(ScrythonRequestHandler, RelevantMixin):
    """Docstring with description and example."""

    _endpoint: str = '/api/path/:param?'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
```

### Mixin Pattern
```python
class ModuleMixin:
    """Provides property accessors for module objects."""

    @property
    def property_name(self) -> ReturnType:
        """Property description from Scryfall docs.

        Returns:
            Description of what this returns
        """
        return self._scryfall_data.get('property_name')
```

### Factory Pattern
```python
class ModuleName:
    """Smart factory that routes to correct endpoint based on kwargs."""

    def __new__(cls, **kwargs):
        if 'param1' in kwargs:
            return Endpoint1(**kwargs)
        elif 'param2' in kwargs:
            return Endpoint2(**kwargs)
        else:
            return DefaultEndpoint(**kwargs)
```

### Test Pattern
```python
def test_endpoint_name():
    """Test endpoint with fixture data."""
    result = ModuleName(param='value')
    assert result.property_name() == expected_value
    assert result.object() == 'object_type'
```

---

## Recommended Implementation Order

1. **Start with Phase 1 (Rulings)** - High priority, commonly requested
2. **Then Phase 2 (Core Catalogs)** - Quick wins, enables validation features
3. **Then Phase 3 (Symbology)** - Medium complexity, useful for advanced features
4. **Then Phase 4 (Complete Catalogs)** - Easy completion of catalog coverage
5. **Then Phase 5 (Migrations)** - Specialized use case, lower priority
6. **Finally Phase 6 (Polish)** - Bring it all together

This order prioritizes user value while building momentum with easier implementations.

---

## Notes

- **Rate Limiting:** Scrython does NOT enforce Scryfall's rate limits (50-100ms between requests). Applications using the new endpoints must implement their own rate limiting.

- **Breaking Changes:** None expected - all new endpoints are additive.

- **Python Version:** Requires Python 3.8+ (walrus operator usage).

- **Dependencies:** No new dependencies required - all endpoints use existing `urllib` and `json` modules.

- **Backwards Compatibility:** All existing code will continue to work. New modules are purely additive.

---

## COMPLETION SUMMARY

**Implementation Date:** November 11, 2025

All 28 remaining Scryfall API endpoints have been successfully implemented, achieving 100% coverage of the Scryfall API!

### What Was Implemented

**Phase 1: Rulings API (5 endpoints) ✅**
- ById, ByMultiverseId, ByMTGOId, ByArenaId, ByCodeNumber
- Rulings smart factory
- 22 comprehensive tests

**Phase 2-4: Catalogs API (20 endpoints) ✅**
Core Catalogs:
- CardNames, CreatureTypes, PlaneswalkerTypes, CardTypes
- KeywordAbilities, KeywordActions, ArtifactTypes, EnchantmentTypes
- LandTypes, SpellTypes

Additional Catalogs:
- ArtistNames, WordBank, Supertypes, BattleTypes
- Powers, Toughnesses, Loyalties, Watermarks
- AbilityWords, FlavorWords

Catalogs smart factory + 36 comprehensive tests

**Phase 3: Symbology API (2 endpoints) ✅**
- All (get all symbols), ParseMana (parse mana costs)
- SymbologyObjectMixin (14 properties), ManaCostMixin (8 properties)
- Symbology smart factory
- 13 comprehensive tests

**Phase 5: Migrations API (2 endpoints) ✅**
- All (paginated list), ById (single migration)
- MigrationsObjectMixin (9 properties)
- Migrations smart factory
- 14 comprehensive tests

### Test Results

**Total Tests:** 273 (100% passing) ✅
- Original tests: 188
- New tests added: 85
- All tests pass
- Type checking: Clean (mypy passes)

### New Modules Created

```
scrython/
├── rulings/
│   ├── __init__.py
│   ├── rulings.py (5 endpoints + factory)
│   └── rulings_mixins.py (RulingsObjectMixin)
├── catalogs/
│   ├── __init__.py
│   └── catalogs.py (20 endpoints + factory)
├── symbology/
│   ├── __init__.py
│   ├── symbology.py (2 endpoints + factory)
│   └── symbology_mixins.py (SymbologyObjectMixin + ManaCostMixin)
└── migrations/
    ├── __init__.py
    ├── migrations.py (2 endpoints + factory)
    └── migrations_mixins.py (MigrationsObjectMixin)
```

### Architecture Consistency

All new modules follow the established Scrython patterns:
- Smart factory classes for intuitive API access
- Mixin-based property accessors
- Comprehensive docstrings with examples
- Full type hints (mypy clean)
- 100% test coverage
- Consistent error handling

### Breaking Changes

**None!** All changes are purely additive. Existing code continues to work without modification.

### Next Steps

The library now has complete Scryfall API coverage! Future work could include:
- Additional examples and documentation
- Performance optimizations
- Enhanced error messages
- Community feedback and refinements

---

## Success Criteria - ALL MET ✅

- ✅ All 49 Scryfall API endpoints implemented
- ✅ 273 tests passing (100% success rate)
- ✅ Comprehensive docstrings with examples on all classes and properties
- ✅ Type hints on all new code (mypy clean)
- ✅ Consistent architecture with existing codebase patterns
- ✅ No regression in existing functionality
- ✅ Code style matches Contributing.md guidelines
- ✅ All nullable fields properly handled with `.get()`
- ✅ All error cases tested
- ✅ Pagination tested for list endpoints

**Scrython 2.0 now provides complete coverage of the Scryfall API!** 🎉
