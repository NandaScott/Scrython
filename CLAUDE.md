# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Scrython is a Python wrapper for the Scryfall API (Magic: The Gathering card database). It provides a clean, Pythonic interface for querying cards, sets, and bulk data from Scryfall's REST API.

## Development Commands

### Testing
```bash
python test.py                  # Run the manual test script
pytest                          # Run pytest tests (if test suite exists)
```

### Installation
```bash
pip install -e .                # Install in development mode
python setup.py install         # Install package
```

## Architecture

### Core Design Pattern: Request Handler + Mixins

The library uses a **base request handler** (`ScrythonRequestHandler`) combined with **mixins** to compose API endpoint classes. This pattern allows different endpoints to share common functionality while maintaining specific behaviors.

**Key components:**

1. **`scrython/base.py`**: Contains `ScrythonRequestHandler` - the base class that handles all HTTP requests to Scryfall API
   - `_build_path()`: Resolves endpoint path parameters (e.g., `:id`, `:code`)
   - `_build_params()`: Constructs query parameters
   - `_fetch()`: Executes HTTP request and handles errors via `ScryfallError`
   - Path parameters use `:param_name` syntax; optional params end with `?` (e.g., `:lang?`)

2. **Mixins** (in `base_mixins.py` and module-specific `*_mixins.py` files):
   - `ScryfallListMixin`: For endpoints returning lists (search results, collections)
   - `ScryfallCatalogMixin`: For endpoints returning catalogs
   - `CoreFieldsMixin`, `GameplayFieldsMixin`, `PrintFieldsMixin`: Card-specific data accessors
   - Mixins provide `@property` accessors to `scryfall_data` dictionary

3. **Smart Factory Classes**: `Cards`, `Sets`, `BulkData`
   - Use `__new__()` to dynamically instantiate the correct endpoint class based on kwargs
   - Example: `Cards(fuzzy="Lightning")` returns `CardsNamed`, while `Cards(search="bolt")` returns `CardsSearch`
   - This provides a single entry point with intelligent routing based on parameters

### Module Structure

```
scrython/
├── base.py              # ScrythonRequestHandler, ScryfallError
├── base_mixins.py       # ScryfallListMixin, ScryfallCatalogMixin
├── utils.py             # Utility functions (e.g., to_object_array)
├── cards/
│   ├── cards.py         # Card endpoint classes + Cards factory
│   └── cards_mixins.py  # Card data accessors (CoreFieldsMixin, etc.)
├── sets/
│   ├── sets.py          # Set endpoint classes + Sets factory
│   └── sets_mixins.py   # Set data accessors
└── bulk_data/
    ├── bulk_data.py     # Bulk data endpoint classes + BulkData factory
    └── bulk_data_mixins.py  # Bulk data accessors
```

### How Requests Work

1. User calls factory: `card = scrython.Cards(fuzzy="Black Lotus")`
2. Factory's `__new__()` selects appropriate class: `CardsNamed`
3. Class inherits from `ScrythonRequestHandler` + relevant mixins
4. `ScrythonRequestHandler.__init__()` runs:
   - `_build_path()` resolves endpoint template (e.g., `/cards/named`)
   - `_build_params()` adds query params (e.g., `?fuzzy=Black+Lotus`)
   - `_fetch()` makes HTTP request, parses JSON into `scryfall_data`
5. Mixin properties provide data access: `card.name` → `scryfall_data['name']`

### Error Handling

- All Scryfall API errors are wrapped in `ScryfallError` (from `scrython/base.py`)
- `ScryfallError` exposes: `status`, `code`, `details`, `type`, `warnings`
- HTTP errors that aren't from Scryfall raise generic `Exception`

## Code Style

From Contributing.md:
- No single character variables (except `f` for files, `i` for iterations)
- Complex code (regex, etc.) needs explanatory comments
- Weird/unexpected code needs comments explaining **why** (not just what)
- 4 spaces for indentation (no tabs)
- Avoid useless comments

## Important Notes

- **No rate limiting**: Library doesn't enforce Scryfall's rate limits - users must handle this themselves (e.g., `time.sleep(0.1)`)
- **No backwards compatibility**: Breaking changes expected as Scryfall API evolves
- **Walrus operator usage**: Code uses `:=` (requires Python 3.8+)
- **Dependencies**: python >= 3.5.3, asyncio >= 3.4.3, aiohttp >= 3.4.4 (though current code uses urllib, not aiohttp)
- **Branches**: `master` is stable/PyPI, `develop` is staging (per Contributing.md, though current branch is `rewrite`)

## Adding New Endpoints

1. Add endpoint class in appropriate module (e.g., `scrython/cards/cards.py`)
2. Set `_endpoint` class variable with path template (use `:param` for path params)
3. Inherit from `ScrythonRequestHandler` + appropriate mixins
4. Update factory class's `__new__()` method to route to your endpoint
5. Add new properties to mixin files if Scryfall returns new fields
