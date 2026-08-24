# Changelog

All notable changes to Scrython will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.0.0] - 2026-08-20

### Added
- **`BulkDataObjectMixin.jsonl_download_uri`**: New accessor for the gzip-compressed JSONL download URI, replacing the removed `download_uri` field.
- **`BulkDataObjectMixin.compressed_size`**: New accessor for the compressed file size in bytes, replacing the removed `size` field.

### Changed
- **`BulkDataObjectMixin.download()`**: Now targets `jsonl_download_uri` and parses the response as newline-delimited JSON (JSONL) rather than a single JSON array.
- **`BulkDataObjectMixin.download()`**: Always decompresses the response instead of decompressing only when the CDN sends `Content-Encoding: gzip`. Scryfall documents `jsonl_download_uri` as hosting the file as `.jsonl.gz`, and `data.scryfall.io` serves it as `content-type: application/gzip` with no `Content-Encoding` header, so the previous header check never fired against a live response. The previous `Accept-Encoding: gzip, identity` request header is also gone; urllib's `identity` default is what this method wants.
- **`BulkDataObjectMixin.download()`**: `chunk_size` now applies only when `progress=True`; the non-progress path streams decompression directly off the response.
- **`ScryfallBulkDataData`**: TypedDict updated to match the current Scryfall bulk-data shape — `download_uri`, `size`, `content_type`, and `content_encoding` removed; `jsonl_download_uri` and `compressed_size` added.

### Removed
- **`BulkDataObjectMixin.download_uri`**: Removed; Scryfall no longer returns this field. Use `jsonl_download_uri` instead.
- **`BulkDataObjectMixin.size`**: Removed; Scryfall no longer returns this field. Use `compressed_size` instead.
- **`BulkDataObjectMixin.content_type`**: Removed; Scryfall no longer returns this field.
- **`BulkDataObjectMixin.content_encoding`**: Removed; Scryfall no longer returns this field.

---

## [2.2.0] - 2026-06-09

### Added
- **`scrython.tags` module**: First-class `Tag` object model for the `art_tags` and `oracle_tags` bulk files. Download the bulk file through the existing `bulk_data.ByType(...).download()` path, then wrap each entry in `scrython.tags.Object` for typed accessors. The nested `taggings` array resolves into typed `scrython.tags.Tagging` objects, with one model covering both art (`illustration_id`) and oracle (`oracle_id`) taggings. Adds `ScryfallTagData` and `ScryfallTaggingData` to `scrython.types`.

---

## [2.1.0] - 2026-05-30

### Added
- **`py.typed` marker**: Scrython now ships a `py.typed` marker file, signaling to type checkers (mypy, pyright, etc.) that the package supports PEP 561 inline type hints. The `Typing :: Typed` PyPI classifier has also been added to `pyproject.toml`.

---

## [2.0.3] - 2026-04-06

### Added
- **Per-endpoint rate limiting**: Scryfall enforces tiered rate limits. `Search`, `Named`, `Random`, and `Collection` endpoints now automatically enforce 2 requests/second; all other endpoints enforce 10 requests/second. See [Scryfall rate limit docs](https://scryfall.com/docs/api/rate-limits).
- **`SlowRateLimiter` subclass**: New rate limiter class for endpoints with stricter limits. Endpoint classes declare their tier via `_rate_limiter_class` class variable.
- **Per-class limiter registry**: Each `RateLimiter` subclass maintains its own global instance, allowing independent rate limits per endpoint category.

### Changed
- `rate_limit_per_second` kwarg now creates a per-instance limiter scoped to the handler's lifecycle. Separate instantiations do not coordinate with each other; pagination within a single handler (`iter_all()`) is properly throttled.
- `reset_global_limiter()` renamed to `reset_all_limiters()`. The old name still works but emits a `DeprecationWarning`.
- `get_global_limiter()` no longer accepts a `calls_per_second` argument. Passing one emits a `DeprecationWarning` and the value is ignored. Rate is determined by the class default.
- Passing `rate_limit_per_second` to `iter_all()` now emits a `UserWarning` and is ignored. The kwarg must be set at construction time.

---

## [2.0.0] - 2025-01-11 (Rewrite Branch)

Major refactoring and modernization of the Scrython library with significant improvements to code quality, type safety, and usability.

### Added

#### TypedDict Integration (Phases 5-6)
- **Full TypedDict type system** from `scrython.types` module
  - `ScryfallCardData` - Complete card object structure
  - `ScryfallSetData` - Complete set object structure
  - `ScryfallBulkDataData` - Complete bulk data object structure
  - `Legalities` - Format legality information
  - `Prices` - Price information in various currencies
  - `ImageUris` - Image URIs for different sizes
  - `PurchaseUris` - Purchase URIs for various vendors
  - `RelatedUris` - Related resource URIs
  - `CardFaceData` - Multi-faced card face data
  - `RelatedCard` - Related card information

- **Refined mixin return types** - Replaced generic `dict[str, Any]` with specific TypedDict types
  - `legalities()` returns `Legalities`
  - `prices()` returns `Prices`
  - `image_uris()` returns `ImageUris | None`
  - `purchase_uris()` returns `PurchaseUris | None`
  - `related_uris()` returns `RelatedUris`

- **Endpoint class type overrides** - Better IDE autocomplete and type checking
  - `cards.Object._scryfall_data: ScryfallCardData`
  - `sets.Object._scryfall_data: ScryfallSetData`
  - `bulk_data.Object._scryfall_data: ScryfallBulkDataData`

#### Bulk Data Download Functionality
- **`download()` method** for all Bulk Data objects
  - Automatic gzip decompression
  - Optional file saving with `filepath` parameter
  - Optional progress bar with `progress=True` (requires `pip install scrython[progress]`)
  - Memory-efficient mode with `return_data=False`
  - Configurable chunk size for downloads

#### Comprehensive Type Hints
- Modern Python 3.10+ type syntax throughout (`X | Y` instead of `Union[X, Y]`)
- All 113 card properties have explicit type annotations
- All 21 set properties have explicit type annotations
- All 11 bulk data properties have explicit type annotations
- Nullable types properly annotated (e.g., `int | None`)
- Complete TypedDict definitions for all Scryfall API response structures
- Full mypy type validation with zero errors

#### Testing Infrastructure
- **113 new property type tests** - Comprehensive parametrized tests validating all properties
- Test coverage for nullable field handling
- Test coverage for nested objects (card faces, related cards)
- Test coverage for bulk data download functionality (6 new tests)
- Test coverage for pagination and caching
- Test coverage for rate limiting
- Total test suite: 394 tests passing (all green)

#### Development Tooling
- **black** - Code formatter with consistent style
- **ruff** - Fast Python linter
- **mypy** - Static type checker
- **pre-commit hooks** - Automatic code quality checks
- GitHub Actions CI/CD configuration
- Type checking enforcement via mypy

#### Documentation
- **CHANGELOG.md** - This file! Complete release notes and migration guide
- **docs/rewrite/REWRITE_HISTORY.md** - Comprehensive 3,843-line rewrite documentation
  - All planning, analysis, and completion documentation in single file
  - Organized chronologically with clear section separators
  - Complete narrative of entire rewrite process (Phases 1-8)
- Enhanced README with bulk data download examples
- Improved inline documentation with official Scryfall descriptions
- All mixins now have comprehensive docstrings (149 properties documented)
- All endpoint classes have detailed docstrings with examples

### Changed

#### Type System Improvements
- Mixin property return types now use specific TypedDict types
- Better IDE autocomplete for nested objects (legalities, prices, image URIs)
- Improved type inference throughout the codebase
- More precise error detection during development

#### Project Organization
- Consolidated rewrite documentation into single `docs/rewrite/REWRITE_HISTORY.md`
- Moved all planning documents from root to `docs/rewrite/` directory
- Cleaner root directory with only essential documentation files
- Better separation of historical documentation from current docs

#### API Structure (Non-Breaking on Rewrite Branch)
- Simplified class names (removed redundant prefixes internally)
  - `CardsNamed` � `Named` (internal)
  - `SetsByCode` � `ByCode` (internal)
  - `BulkDataByType` � `ByType` (internal)
- Direct class imports from submodules instead of factory pattern
- Read-only `scryfall_data` property returns `SimpleNamespace` instead of dict
  - Provides dot-notation access: `card.scryfall_data.name`
  - Prevents accidental mutation of internal data
  - Cached for performance

#### Code Quality
- All code formatted with black (line length: 100)
- All code passes ruff linting checks
- All code passes mypy type checking
- Modern Python 3.10+ features utilized
- Consistent naming conventions throughout

#### README Updates
- Added bulk data download examples
- Updated rate limiting guidance
- Added progress bar usage examples
- Clarified caching recommendations
- Added memory-efficient download examples

### Fixed

#### Critical Bugs
- **Nullable property KeyError** - All nullable properties now use `.get()` method
  - Fixed 74 nullable properties across `cards_mixins.py` and `sets_mixins.py`
  - Properties gracefully return `None` when keys are missing from API responses
  - Prevents crashes when Scryfall API returns incomplete data

- **`to_object_array` utility** - Now handles missing keys for nullable array fields
  - `all_parts` and `card_faces` properties work correctly when data is missing

- **Test fixtures** - Added missing required fields to mock API responses
  - Added `uri` field to bulk_data/by_id.json fixture

#### Pre-commit Configuration
- Fixed hooks to only check `scrython/` and `tests/` directories
- Added `typing-extensions` dependency for mypy
- Configured proper file patterns for each hook

### Development Changes

#### Python Version
- **Python 3.10+ now required** (was 3.5.3+)
- Leverages modern type hint syntax and language features

#### Project Structure
- Reorganized into clear module hierarchy
- Mixins separated from endpoint classes
- Comprehensive test organization by module
- Fixtures organized by endpoint type

#### Testing Improvements
- 188 total tests (75 original + 113 new property tests)
- Mock-based testing with realistic Scryfall responses
- Comprehensive error case coverage
- Parametrized tests for systematic property validation

---

## [1.8.0] - Previous Release (Master Branch)

See git history for changes in previous releases.

---

## Upcoming Changes

### Future Releases (Roadmap)

The Rulings, Catalog, Symbology, and Migration endpoints, plus the built-in
TTL caching layer, have all shipped. Remaining roadmap items:

#### Near-term
- Improve error messages with more context
- Add retry logic with exponential backoff
- Consider async/await support for concurrent requests

#### Version 3.0.0 (Major)
- Complete Scryfall API coverage across all published endpoints
- Potential breaking changes for improved API design
- GraphQL support if Scryfall adds it
- Performance optimizations

---

## Migration Guide (For Rewrite Branch)

### From 1.x to 2.0

#### 1. Python Version Upgrade
**Required:** Upgrade to Python 3.10 or higher

```bash
# Check your Python version
python --version  # Should be 3.10.0 or higher
```

#### 2. No API Breaking Changes Yet
The rewrite branch maintains backward compatibility with import patterns.
Factory pattern still works, though direct imports are recommended for future compatibility.

```python
# Both still work on rewrite branch:
import scrython
card = scrython.Cards(fuzzy='Lightning Bolt')  # Still works

from scrython.cards import Named
card = Named(fuzzy='Lightning Bolt')  # Recommended
```

#### 3. scryfall_data Access (Recommended Update)
The `scryfall_data` property now returns a read-only `SimpleNamespace`.

```python
# Old style (still works, but avoid mutations):
card.scryfall_data.name  #  Reading works
card._scryfall_data['name']  #  Direct access still works

# Mutations no longer affect internal data:
card.scryfall_data.name = 'Modified'  # � Doesn't affect internal data
```

#### 4. Bulk Data Downloads (New Feature)
Take advantage of the new built-in download functionality:

```python
from scrython.bulk_data import ByType

# New way (recommended):
bulk = ByType(type='oracle_cards')
cards = bulk.download()  # Automatic decompression!

# With progress bar:
cards = bulk.download(progress=True)  # Requires: pip install scrython[progress]

# Save to file:
bulk.download(filepath='oracle_cards.json')
```

#### 5. Development Setup (If Contributing)
New development dependencies and tools:

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Or install individually
pip install black ruff mypy pytest pytest-cov pre-commit

# Setup pre-commit hooks
pre-commit install

# Run quality checks
black scrython tests
ruff check scrython tests
mypy scrython
pytest
```

---

## Contributors

- **NandaScott** - Original author and maintainer
- **Claude (Anthropic)** - Refactoring assistance for 2.0 rewrite

---

## Links

- **GitHub Repository**: https://github.com/NandaScott/Scrython
- **PyPI Package**: https://pypi.org/project/scrython/
- **Scryfall API Documentation**: https://scryfall.com/docs/api
- **Issue Tracker**: https://github.com/NandaScott/Scrython/issues
