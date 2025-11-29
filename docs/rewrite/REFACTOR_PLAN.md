# Multiphase Plan for Scrython Improvements

This document outlines a comprehensive plan to address all items in IMPROVEMENTS.md and modernize the Scrython codebase.

## Key Decisions

- **Import Structure**: Remove factory pattern, rename classes for direct imports
- **Python Version**: Target Python 3.10+ for modern type hints
- **API Endpoints**: Focus on core improvements first, document missing endpoints
- **Dev Tooling**: Add black, ruff, mypy, pre-commit hooks

---

## Phase 1: Project Infrastructure & Tooling Setup
**Goal:** Modernize development environment and tooling

### 1.1 Update Python version requirements
- Update `setup.py`: require Python ≥3.10
- Update all type hints to use modern syntax (`X | Y` instead of `Union[X, Y]`)
- Remove outdated asyncio/aiohttp dependencies (currently not used in code)

### 1.2 Add development tooling
- Create `pyproject.toml` with configuration for:
  - black (code formatter)
  - ruff (fast linter)
  - mypy (type checker)
  - pytest (test configuration)
- Create `.pre-commit-config.yaml` with hooks for:
  - black (auto-format code)
  - ruff (lint checks)
  - mypy (type checking)
  - trailing-whitespace, end-of-file-fixer
- Update `setup.py` with dev dependencies: `pip install -e .[dev]`

### 1.3 Update Contributing.md
Add comprehensive sections:
- **Development Environment Setup**
  - Python version requirements (3.10+)
  - venv creation: `python -m venv venv`
  - Activation: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
  - Install dev dependencies: `pip install -e .[dev]`
- **Running Tests**
  - `pytest` - Run full test suite
  - `pytest tests/test_cards.py` - Run specific test file
  - `pytest -v` - Verbose output
  - `pytest --cov=scrython --cov-report=html` - With coverage report
  - `python test.py` - Manual integration test
- **Code Quality Tools**
  - Formatting: `black .`
  - Linting: `ruff check .`
  - Type checking: `mypy scrython`
  - Pre-commit hooks: `pre-commit install` and `pre-commit run --all-files`
- **Project Architecture**
  - Explanation of request handler + mixin pattern
  - How to add new endpoints
  - How to add new tests
- **Branch Strategy**
  - Update: current development on `rewrite` branch
  - Clarify merge to `main` workflow

**Estimated Effort**: 2-3 hours

---

## Phase 2: Architecture Refactor - Remove Factory Pattern
**Goal:** Simplify imports and remove magic routing (BREAKING CHANGE)

### 2.1 Rename all endpoint classes

**Cards module** (`scrython/cards/cards.py`):
- `CardsNamed` → `Named`
- `CardsSearch` → `Search`
- `CardsAutocomplete` → `Autocomplete`
- `CardsRandom` → `Random`
- `CardsCollection` → `Collection`
- `CardsByCodeNumber` → `ByCodeNumber`
- `CardsByMultiverseId` → `ByMultiverseId`
- `CardsByMTGOId` → `ByMTGOId`
- `CardsByArenaId` → `ByArenaId`
- `CardsByTCGPlayerId` → `ByTCGPlayerId`
- `CardsByCardMarketId` → `ByCardMarketId`
- `CardsById` → `ById`

**Sets module** (`scrython/sets/sets.py`):
- `AllSets` → `All`
- `SetsByCode` → `ByCode`
- `SetsByTCGPlayerId` → `ByTCGPlayerId`
- `SetsById` → `ById`

**BulkData module** (`scrython/bulk_data/bulk_data.py`):
- `AllBulkData` → `All`
- `BulkDataById` → `ById`
- `BulkDataByType` → `ByType`

### 2.2 Remove factory classes
- Delete `Cards` class with `__new__()` routing logic
- Delete `Sets` class with `__new__()` routing logic
- Delete `BulkData` class with `__new__()` routing logic

### 2.3 Update imports
- Update `scrython/__init__.py` to export all endpoint classes directly
- Update `scrython/cards/__init__.py` to export: `Named`, `Search`, `Autocomplete`, etc.
- Update `scrython/sets/__init__.py` to export: `All`, `ByCode`, `ById`, etc.
- Update `scrython/bulk_data/__init__.py` to export: `All`, `ById`, `ByType`

**New usage patterns**:
```python
# Old (factory pattern):
import scrython
card = scrython.Cards(fuzzy='Lightning Bolt')

# New (direct imports):
from scrython.cards import Named
card = Named(fuzzy='Lightning Bolt')

# Or import from top-level:
from scrython import cards
card = cards.Named(fuzzy='Lightning Bolt')
```

### 2.4 Update all tests
- `tests/test_cards.py`: Replace factory calls with direct class imports
- `tests/test_sets.py`: Replace factory calls with direct class imports
- `tests/test_bulk_data.py`: Replace factory calls with direct class imports
- `tests/test_base.py`: Update any factory-related tests
- Remove factory routing tests (no longer applicable)

### 2.5 Update documentation
- Update README.md with new import examples for all endpoint classes
- Update docstrings in all endpoint classes with correct class names
- Add migration guide section to README for users upgrading

**Estimated Effort**: 4-6 hours

---

## Phase 3: Read-Only scryfall_data with SimpleNamespace
**Goal:** Prevent accidental mutation while maintaining dot-notation access

### 3.1 Modify ScrythonRequestHandler (`scrython/base.py`)
- Rename `scryfall_data: Dict[str, Any]` → `_scryfall_data: dict[str, Any]` (private)
- Add property:
  ```python
  @property
  def scryfall_data(self) -> types.SimpleNamespace:
      """Read-only access to Scryfall API response data.

      Returns a SimpleNamespace object allowing dot-notation access.
      This is a read-only view - modifications will not affect internal data.
      """
      if not hasattr(self, '_scryfall_namespace'):
          self._scryfall_namespace = types.SimpleNamespace(**self._scryfall_data)
      return self._scryfall_namespace
  ```
- Update `_fetch()` method to invalidate cache when new data is fetched

### 3.2 Update all mixins
- All mixin properties continue accessing `self._scryfall_data['key']` for performance
- No changes needed to property implementations
- Update any docstrings that reference `scryfall_data` to clarify read-only access

### 3.3 Add tests (`tests/test_base.py`)
- Test that `scryfall_data` returns SimpleNamespace type
- Test that mutations don't affect internal data:
  ```python
  card.scryfall_data.name = "Modified"
  assert card.name != "Modified"  # Internal data unchanged
  ```
- Test dot-notation access: `assert card.scryfall_data.name == card.name`
- Test that property is cached (same object returned on multiple accesses)

### 3.4 Update documentation
- Update README with `scryfall_data` usage examples
- Document the read-only nature prominently
- Show dot-notation access examples

**Estimated Effort**: 2-3 hours

---

## Phase 4: Comprehensive Type Hints (Python 3.10+)
**Goal:** Strong typing throughout the codebase

### 4.1 Create TypedDict definitions
- New file: `scrython/types.py`
- Define comprehensive TypedDicts for Scryfall API responses:
  ```python
  from typing import TypedDict, NotRequired

  class ScryfallCardData(TypedDict):
      # Required fields
      id: str
      name: str
      # ... all required fields

      # Optional/nullable fields
      colors: NotRequired[list[str]]
      mana_cost: NotRequired[str]
      # ... all optional fields
  ```
- Create `ScryfallSetData`, `ScryfallBulkDataData`, etc.
- Create TypedDicts for nested objects (CardFace, RelatedCard, etc.)

### 4.2 Add return type hints to all properties

**Cards mixins** (`scrython/cards/cards_mixins.py`):
- CoreFieldsMixin: Add return types to all 17 properties
- GameplayFieldsMixin: Add return types to all 23 properties
- PrintFieldsMixin: Add return types to all 32 properties
- CardFaceMixin: Add return types to all 23 properties
- RelatedCardsObjectMixin: Add return types to all 5 properties

Examples:
```python
@property
def name(self) -> str:
    return self._scryfall_data['name']

@property
def colors(self) -> list[str] | None:
    return self._scryfall_data.get('colors')

@property
def all_parts(self) -> list[dict[str, Any]] | None:
    return self._scryfall_data.get('all_parts')
```

**Sets mixins** (`scrython/sets/sets_mixins.py`):
- Add return types to all properties (~20 properties)

**BulkData mixins** (`scrython/bulk_data/bulk_data_mixins.py`):
- Add return types to all properties (~8 properties)

**List/Catalog mixins** (`scrython/base_mixins.py`):
- Add return types to all methods

### 4.3 Type hint all endpoint class methods
- Add parameter type hints to all `__init__()` methods
- Add return type hints to any custom methods
- Update base class `ScrythonRequestHandler` method signatures

### 4.4 Configure mypy
Add to `pyproject.toml`:
```toml
[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

### 4.5 Run mypy and fix all errors
- Run `mypy scrython` and address all type errors
- May need to add `# type: ignore` comments for complex dynamic cases
- Ensure all tests pass after type hint additions

**Estimated Effort**: 3-4 hours

---

## Phase 5: BulkData Download Functionality
**Goal:** Built-in download support for bulk data files

### 5.1 Add download() method to BulkDataObjectMixin

Location: `scrython/bulk_data/bulk_data_mixins.py`

```python
import gzip
import json
from urllib.request import urlopen
from typing import Any

def download(
    self,
    filepath: str | None = None,
    return_data: bool = True,
    chunk_size: int = 8192
) -> list[dict[str, Any]] | None:
    """Download and parse bulk data file from Scryfall.

    Args:
        filepath: Optional path to save the decompressed JSON file.
                 If None, file is not saved to disk.
        return_data: If True, return parsed JSON data. If False and
                    filepath is provided, only saves file.
        chunk_size: Download chunk size in bytes (default 8192)

    Returns:
        List of card/set objects if return_data=True, otherwise None.

    Raises:
        Exception: If download fails or file is invalid.

    Example:
        >>> bulk = BulkDataByType(type='oracle_cards')
        >>> cards = bulk.download()
        >>> print(f"Downloaded {len(cards)} cards")

        >>> # Or save to file:
        >>> bulk.download(filepath='oracle_cards.json', return_data=False)
    """
    download_url = self.download_uri()

    # Download with gzip decompression
    with urlopen(download_url) as response:
        with gzip.GzipFile(fileobj=response) as gz_file:
            data = gz_file.read()

    # Parse JSON
    parsed_data = json.loads(data.decode('utf-8'))

    # Save to file if requested
    if filepath:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, indent=2)

    # Return data if requested
    return parsed_data if return_data else None
```

### 5.2 Add optional progress bar support
- Add optional dependency: `tqdm`
- Add `progress: bool = False` parameter
- Wrap download with tqdm progress bar if requested
- Document in setup.py as extra: `pip install scrython[progress]`

### 5.3 Add tests (`tests/test_bulk_data.py`)
- Mock `urlopen` to return test gzip data
- Test basic download with `return_data=True`
- Test file saving with `filepath` parameter
- Test error cases:
  - Network failure
  - Invalid gzip data
  - Invalid JSON
  - Permission error on file write
- Test that method works with all bulk data types

### 5.4 Update documentation
- Add download() method to docstrings
- Update README with bulk data download examples:
  ```python
  from scrython.bulk_data import ByType

  # Download oracle cards
  bulk = ByType(type='oracle_cards')
  cards = bulk.download()

  # Or save to file
  bulk.download(filepath='oracle_cards.json')
  ```

**Estimated Effort**: 2-3 hours

---

## Phase 6: Comprehensive Property Type Testing
**Goal:** Every property tested with expected type validation

### 6.1 Create parametrized property tests

New file: `tests/test_property_types.py`

Structure:
```python
import pytest
from scrython.cards import Named
from scrython.sets import ByCode
from scrython.bulk_data import ByType

# Card property test data
CARD_PROPERTIES = [
    # (property_name, expected_type, nullable, test_card_kwargs)
    ("name", str, False, {"exact": "Lightning Bolt"}),
    ("colors", list, True, {"exact": "Lightning Bolt"}),
    ("cmc", (int, float), False, {"exact": "Lightning Bolt"}),
    ("mana_cost", str, True, {"exact": "Lightning Bolt"}),
    # ... all ~149 card properties
]

@pytest.mark.parametrize("prop,expected_type,nullable,card_kwargs", CARD_PROPERTIES)
def test_card_property_type(mock_scryfall_response, prop, expected_type, nullable, card_kwargs):
    """Test that each card property returns the expected type."""
    card = Named(**card_kwargs)
    value = getattr(card, prop)

    if nullable and value is None:
        return  # None is acceptable for nullable fields

    assert isinstance(value, expected_type), \
        f"Property '{prop}' returned {type(value)} instead of {expected_type}"
```

### 6.2 Test all card properties (~149 properties)

Create test data for:
- **CoreFieldsMixin**: 17 properties
  - arena_id, id, lang, mtgo_id, mtgo_foil_id, multiverse_ids, tcgplayer_id, tcgplayer_etched_id, cardmarket_id, object, layout, oracle_id, prints_search_uri, rulings_uri, scryfall_uri, uri

- **GameplayFieldsMixin**: 23 properties
  - all_parts, card_faces, cmc, color_identity, color_indicator, colors, defense, edhrec_rank, hand_modifier, keywords, legalities, life_modifier, loyalty, mana_cost, name, oracle_text, penny_rank, power, produced_mana, reserved, toughness, type_line

- **PrintFieldsMixin**: 32 properties
  - artist, artist_ids, attraction_lights, booster, border_color, card_back_id, collector_number, content_warning, digital, finishes, flavor_name, flavor_text, frame_effects, frame, full_art, games, highres_image, illustration_id, image_status, image_uris, oversized, preview, prices, printed_name, printed_text, printed_type_line, promo, promo_types, purchase_uris, rarity, related_uris, released_at, reprint, security_stamp, set_name, set_search_uri, set_type, set_uri, set, story_spotlight, textless, variation, variation_of, watermark

- **CardFaceMixin**: 23 properties (nested object)

- **RelatedCardsObjectMixin**: 5 properties

- **List mixin methods**: data(), has_more(), next_page(), total_cards(), etc.

### 6.3 Test all sets properties (~20 properties)
- Similar parametrized approach for Sets endpoint classes
- Test all SetsMixin properties

### 6.4 Test all bulk_data properties (~8 properties)
- Test BulkDataObjectMixin properties
- Test list mixin for AllBulkData

### 6.5 Test nullable behavior
- Properties marked as nullable should gracefully return None when key is missing
- Required properties should either:
  - Always be present in real Scryfall responses, OR
  - Raise KeyError with helpful message if missing

### 6.6 Use realistic mock data
- Update `conftest.py` with comprehensive mock Scryfall responses
- Ensure mocks include all property types (strings, arrays, nested objects, null values)
- Consider using real Scryfall API responses as test fixtures

**Estimated Effort**: 4-6 hours

---

## Phase 7: Documentation & Future Planning
**Goal:** Document current state and future roadmap

### 7.1 Create API_CHECKLIST.md

Document all Scryfall API endpoints with implementation status:

```markdown
# Scryfall API Coverage Checklist

## Cards ✅ COMPLETE (13/13 endpoints)
- [x] GET /cards/search - `cards.Search`
- [x] GET /cards/named - `cards.Named`
- [x] GET /cards/autocomplete - `cards.Autocomplete`
- [x] GET /cards/random - `cards.Random`
- [x] POST /cards/collection - `cards.Collection`
- [x] GET /cards/:code/:number - `cards.ByCodeNumber`
- [x] GET /cards/multiverse/:id - `cards.ByMultiverseId`
- [x] GET /cards/mtgo/:id - `cards.ByMTGOId`
- [x] GET /cards/arena/:id - `cards.ByArenaId`
- [x] GET /cards/tcgplayer/:id - `cards.ByTCGPlayerId`
- [x] GET /cards/cardmarket/:id - `cards.ByCardMarketId`
- [x] GET /cards/:id - `cards.ById`

## Sets ✅ COMPLETE (4/4 endpoints)
- [x] GET /sets - `sets.All`
- [x] GET /sets/:code - `sets.ByCode`
- [x] GET /sets/tcgplayer/:id - `sets.ByTCGPlayerId`
- [x] GET /sets/:id - `sets.ById`

## Rulings ❌ NOT IMPLEMENTED (0/5 endpoints) - HIGH PRIORITY
- [ ] GET /cards/:id/rulings
- [ ] GET /cards/multiverse/:id/rulings
- [ ] GET /cards/mtgo/:id/rulings
- [ ] GET /cards/arena/:id/rulings
- [ ] GET /cards/:code/:number/rulings

## Symbology ❌ NOT IMPLEMENTED (0/2 endpoints) - MEDIUM PRIORITY
- [ ] GET /symbology
- [ ] GET /symbology/parse-mana

## Catalogs ❌ NOT IMPLEMENTED (0/15 endpoints) - MEDIUM PRIORITY
- [ ] GET /catalog/card-names
- [ ] GET /catalog/artist-names
- [ ] GET /catalog/word-bank
- [ ] GET /catalog/creature-types
- [ ] GET /catalog/planeswalker-types
- [ ] GET /catalog/land-types
- [ ] GET /catalog/artifact-types
- [ ] GET /catalog/enchantment-types
- [ ] GET /catalog/spell-types
- [ ] GET /catalog/powers
- [ ] GET /catalog/toughnesses
- [ ] GET /catalog/loyalties
- [ ] GET /catalog/watermarks
- [ ] GET /catalog/keyword-abilities
- [ ] GET /catalog/keyword-actions
- [ ] GET /catalog/ability-words

## Card Migrations ❌ NOT IMPLEMENTED (0/2 endpoints) - LOW PRIORITY
- [ ] GET /migrations/:id
- [ ] GET /migrations/all

## Bulk Data ✅ COMPLETE (3/3 endpoints)
- [x] GET /bulk-data - `bulk_data.All`
- [x] GET /bulk-data/:id - `bulk_data.ById`
- [x] GET /bulk-data/:type - `bulk_data.ByType`

---

## Implementation Priority

### High Priority
- **Rulings**: Commonly used for competitive play and rules questions

### Medium Priority
- **Symbology**: Useful for mana cost parsing and validation
- **Catalogs**: Useful for autocomplete, validation, and deckbuilding tools

### Low Priority
- **Card Migrations**: Specialized use case for tracking card ID changes
```

### 7.2 Update IMPROVEMENTS.md
- Mark completed items with ✅
- Add dates of completion
- Add new improvement ideas discovered during refactor:
  - Consider async/await support for concurrent requests
  - Add caching layer for frequently accessed cards
  - Add retry logic with exponential backoff
  - Consider GraphQL support if Scryfall adds it

### 7.3 Update README.md

Major updates:
- **Requirements section**: Python 3.10+ (breaking change from 3.5.3)
- **Installation section**: Include dev dependencies option
- **Usage section**: Complete rewrite with new import patterns
  ```python
  # Cards
  from scrython.cards import Named, Search, Random

  card = Named(fuzzy='Lightning Bolt')
  print(card.name)  # "Lightning Bolt"
  print(card.mana_cost)  # "{R}"

  # Bulk Data with download
  from scrython.bulk_data import ByType

  bulk = ByType(type='oracle_cards')
  cards = bulk.download()
  print(f"Downloaded {len(cards)} cards")
  ```
- **Migration Guide section**: How to upgrade from 2.x to 3.0
- **scryfall_data access**: Document read-only SimpleNamespace
- **API Coverage**: Link to API_CHECKLIST.md

### 7.4 Create CHANGELOG.md

Version 3.0.0 changelog:
```markdown
# Changelog

## [3.0.0] - YYYY-MM-DD

### Breaking Changes
- **Python 3.10+ required** (was 3.5.3+)
- **Factory pattern removed** - must import endpoint classes directly
  - Old: `scrython.Cards(fuzzy='bolt')`
  - New: `from scrython.cards import Named; Named(fuzzy='bolt')`
- **scryfall_data is now read-only** - returns SimpleNamespace instead of dict
- **All endpoint classes renamed** - removed redundant prefixes
  - `CardsNamed` → `Named`, `SetsByCode` → `ByCode`, etc.

### Added
- Bulk data download functionality (`bulk_data.download()` method)
- Comprehensive type hints using Python 3.10+ syntax
- Development tooling: black, ruff, mypy, pre-commit hooks
- Read-only `scryfall_data` property with dot-notation access
- Comprehensive property type testing
- API_CHECKLIST.md documenting endpoint coverage

### Changed
- Updated Contributing.md with complete development setup guide
- Modern type hints throughout (use `X | Y` instead of `Union[X, Y]`)
- Improved error messages

### Fixed
- Import structure no longer requires redundant module names
```

### 7.5 Version bump
- Update `setup.py`: version = "3.0.0"
- Update `scrython/__init__.py`: `__version__ = "3.0.0"`

**Estimated Effort**: 2-3 hours

---

## Total Implementation Effort

**Estimated Total**: 19-28 hours

## Breaking Changes Summary

Users upgrading from Scrython 2.x will need to:

1. **Upgrade Python** to version 3.10 or higher

2. **Change all imports** from factory pattern to direct class imports:
   ```python
   # Old (2.x):
   import scrython
   card = scrython.Cards(fuzzy='Lightning Bolt')

   # New (3.0):
   from scrython.cards import Named
   card = Named(fuzzy='Lightning Bolt')
   ```

3. **Update scryfall_data access** if directly modifying:
   ```python
   # Old (2.x):
   card.scryfall_data['name'] = 'Modified'  # Could mutate

   # New (3.0):
   card.scryfall_data.name  # Read-only, dot-notation
   # Mutations will not affect internal data
   ```

4. **Review any code relying on factory pattern routing** - no longer automatically selects endpoint based on kwargs

---

## Testing Strategy

After each phase:
1. Run full test suite: `pytest -v`
2. Run type checker: `mypy scrython`
3. Run linter: `ruff check .`
4. Check code formatting: `black --check .`
5. Verify all pre-commit hooks pass: `pre-commit run --all-files`
6. Run manual integration tests: `python test.py`

Before final release:
1. Test with real Scryfall API (not just mocks)
2. Verify rate limiting guidance in docs
3. Test on multiple platforms (Linux, macOS, Windows)
4. Test with Python 3.10, 3.11, 3.12, 3.13
5. Generate and review coverage report
6. Review all docstrings for accuracy

---

## Success Criteria

- [ ] All items in IMPROVEMENTS.md addressed
- [ ] All tests passing (expect 100+ tests after Phase 6)
- [ ] Type checker passes with no errors (mypy strict mode)
- [ ] Code coverage ≥90%
- [ ] All pre-commit hooks configured and passing
- [ ] Documentation complete and accurate
- [ ] Breaking changes clearly documented
- [ ] Migration guide available
- [ ] Version 3.0.0 ready for release
