# Scrython 2.0 Implementation Plan

**Project**: Scrython - Python wrapper for Scryfall API
**Branch**: `rewrite`
**Status**: ✅ READY FOR BETA RELEASE - Phases 1-3 complete, Phase 4 partial
**Last Updated**: 2025-01-08

---

## Quick Reference

- **ANALYSIS.md** - Detailed UX analysis and API comparison
- **API_CHECKLIST.md** - Complete endpoint and field inventory
- **This Document** - Step-by-step implementation roadmap

---

## Overview

Scrython 2.0 is a complete rewrite using a factory pattern and mixin architecture. The core implementation is solid but has critical bugs and missing API compliance features. This plan outlines all work needed to bring it to production quality.

**Current State** (Ready for Beta Release):
- ✅ 19/47 Scryfall endpoints implemented (Cards, Sets, Bulk Data)
- ✅ 84/84 tests passing
- ✅ All 4 critical property name typos FIXED
- ✅ Rate limiting guidance added (README + docstrings)
- ✅ 40/149 properties documented (core + gameplay fields)
- ✅ API compliance complete (User-Agent, error messages, caching guidance)
- ⏸️ 28 endpoints not yet implemented (Rulings, Catalogs, Symbology, Migrations) - Future work
- ⏸️ 109 properties pending docstrings - Future work

---

## Phase 1: Analysis & Documentation ✅ COMPLETE

**Status**: ✅ Complete
**Date Completed**: 2025-01-08

### Deliverables Created:
1. ✅ `ANALYSIS.md` - Comprehensive UX and API comparison
2. ✅ `API_CHECKLIST.md` - Complete endpoint and field inventory
3. ✅ `tests/` directory - 84 passing tests with mocked responses
4. ✅ This document (`IMPLEMENTATION_PLAN.md`)

### Key Findings:
- 4 critical property name typos in `cards_mixins.py`
- Missing `self` parameter bug in `sets_mixins.py` (fixed during testing)
- No rate limiting implementation (Scryfall requires 50-100ms delays)
- User-Agent header doesn't follow API guidelines
- 150+ properties missing docstrings
- 28 endpoints not yet implemented

---

## Phase 2: Critical Bug Fixes

**Priority**: 🔴 CRITICAL - Must complete before any release
**Estimated Time**: 30 minutes
**Dependencies**: None

### Objectives:
Fix bugs that break core functionality or violate Python conventions.

---

### Task 2.1: Fix Property Name Typos in cards_mixins.py

**File**: `/home/nanda/Coding/Scrython/scrython/cards/cards_mixins.py`

**Changes Required**:

1. **Line 137** - GameplayFieldsMixin
   ```python
   # BEFORE:
   @property
   def mana_costmissing(self):
       return self.scryfall_data['mana_costmissing']

   # AFTER:
   @property
   def mana_cost(self):
       return self.scryfall_data['mana_cost']
   ```

2. **Line 242** - PrintFieldsMixin
   ```python
   # BEFORE:
   @property
   def illustration_idfield(self):
       return self.scryfall_data['illustration_idfield']

   # AFTER:
   @property
   def illustration_id(self):
       return self.scryfall_data['illustration_id']
   ```

3. **Line 258** - PrintFieldsMixin
   ```python
   # BEFORE:
   @property
   def pricesas(self):
       return self.scryfall_data['pricesas']

   # AFTER:
   @property
   def prices(self):
       return self.scryfall_data['prices']
   ```

4. **Line 411** - CardFaceMixin
   ```python
   # BEFORE:
   @property
   def mana_costmana(self):
       return self.scryfall_data['mana_costmana']

   # AFTER:
   @property
   def mana_cost(self):
       return self.scryfall_data['mana_cost']
   ```

**Verification**:
```bash
source venv/bin/activate
pytest tests/test_cards.py::TestCardsMixins -v
```

All tests should still pass after changes.

---

### Task 2.2: Fix warnings() Method in ScryfallError

**File**: `/home/nanda/Coding/Scrython/scrython/base.py`
**Line**: 31

**Issue**: `warnings()` is a method but should be a property for consistency

**Change**:
```python
# BEFORE (line 31):
def warnings(self):
    return self._warnings

# AFTER:
@property
def warnings(self):
    return self._warnings
```

**Verification**:
```bash
pytest tests/test_base.py::TestScryfallError -v
```

---

### Task 2.3: Add Explicit urllib.error Import

**File**: `/home/nanda/Coding/Scrython/scrython/base.py`
**Line**: 1-3

**Issue**: Using `urllib.error.HTTPError` without importing `urllib.error`

**Change**:
```python
# BEFORE:
import json
from urllib.request import Request, urlopen
import urllib.parse

# AFTER:
import json
import urllib.error
import urllib.parse
from urllib.request import Request, urlopen
```

**Note**: Code works currently because full path is used, but this is cleaner and more explicit.

---

### Task 2.4: Verify All Tests Still Pass

**Command**:
```bash
source venv/bin/activate
pytest -v
```

**Expected**: 84/84 tests passing

**If failures occur**: Review changes, ensure no typos introduced

---

## Phase 3: API Compliance & Best Practices

**Priority**: 🟠 HIGH - Required for responsible API usage
**Estimated Time**: 2-3 hours
**Dependencies**: Phase 2 complete

### Objectives:
Ensure Scrython follows Scryfall API requirements and best practices.

---

### Task 3.1: Add Rate Limiting Documentation

**Files to Update**:
1. `README.md`
2. `scrython/base.py` (add class docstring)

**README.md Changes**:

Add new section after installation instructions:

```markdown
## ⚠️ Important: Rate Limiting

**Scryfall requires 50-100 milliseconds delay between requests** (~10 requests/second maximum).

Excessive requests can result in temporary or permanent IP bans. You are responsible for implementing rate limiting in your application.

### Example with Rate Limiting:

```python
import scrython
import time

# Search for cards with proper delays
cards_to_fetch = ['Lightning Bolt', 'Counterspell', 'Black Lotus']

for card_name in cards_to_fetch:
    card = scrython.Cards(fuzzy=card_name)
    print(f"{card.name} - {card.set}")

    # IMPORTANT: Add delay between requests
    time.sleep(0.1)  # 100ms delay
```

### Better: Use Bulk Data for Large Datasets

For large-scale data processing, use Scryfall's bulk data downloads instead:

```python
bulk = scrython.BulkData(type='default_cards')
download_url = bulk.download_uri

# Download and process locally
# (Bulk data files are updated every 12 hours)
```

### Caching Recommendations

- Cache responses for at least 24 hours
- Card prices become unreliable after 24 hours
- Consider downloading bulk data for offline processing
```

**scrython/base.py Changes**:

Add class docstring to `ScrythonRequestHandler`:

```python
class ScrythonRequestHandler:
    """
    Base class for all Scryfall API requests.

    This class handles HTTP communication with the Scryfall API including
    path building, query parameter encoding, and error handling.

    IMPORTANT - Rate Limiting:
        Scryfall requires 50-100ms delay between requests. This class does
        NOT enforce rate limiting - you must implement delays in your code.

        Example:
            import time
            card1 = scrython.Cards(fuzzy='Lightning Bolt')
            time.sleep(0.1)  # 100ms delay
            card2 = scrython.Cards(fuzzy='Counterspell')

    API Requirements:
        - User-Agent header is required (default: 'Scrython/2.0')
        - Accept header is required (default: 'application/json')
        - HTTPS with TLS 1.2+ is required
    """
    scryfall_data = {}
    # ... rest of class
```

---

### Task 3.2: Improve User-Agent Header

**File**: `/home/nanda/Coding/Scrython/scrython/base.py`

**Current Issue**:
- Hardcoded version
- No contact information
- Can't be customized

**Changes**:

1. Update default User-Agent (line 36):
```python
# BEFORE:
_user_agent = 'Scrython/2.0'

# AFTER:
_user_agent = 'Scrython/2.0 (https://github.com/NandaScott/Scrython)'
```

2. Add class method to allow customization:
```python
class ScrythonRequestHandler:
    scryfall_data = {}
    _user_agent = 'Scrython/2.0 (https://github.com/NandaScott/Scrython)'
    _accept = 'application/json'
    _content_type = 'application/json'
    _endpoint = ''

    @classmethod
    def set_user_agent(cls, user_agent: str):
        """
        Set a custom User-Agent header for all Scrython requests.

        Scryfall recommends identifying your application in the User-Agent.

        Args:
            user_agent: Custom User-Agent string

        Example:
            scrython.Cards.set_user_agent('MyMTGApp/1.0 (contact@example.com)')
        """
        cls._user_agent = user_agent
```

3. Update README.md with example:
```markdown
### Custom User-Agent (Recommended)

Scryfall requests that applications identify themselves with a custom User-Agent:

```python
import scrython

# Set custom User-Agent for your application
scrython.Cards.set_user_agent('MyMTGApp/1.0 (contact@example.com)')

# All subsequent requests will use your custom User-Agent
card = scrython.Cards(fuzzy='Black Lotus')
```
```

---

### Task 3.3: Improve Factory Error Messages

**Files to Update**:
1. `scrython/cards/cards.py` - line 86
2. `scrython/sets/sets.py` - (add error if no default matches)
3. `scrython/bulk_data/bulk_data.py` - (add error if no default matches)

**Cards Factory** (`scrython/cards/cards.py`):
```python
# BEFORE (line 86):
raise Exception('No mode found')

# AFTER:
raise ValueError(
    "No valid parameters provided to Cards factory.\n"
    "Use one of the following:\n"
    "  - fuzzy='name' or exact='name' - Get card by name\n"
    "  - search='query' - Search with Scryfall syntax\n"
    "  - autocomplete='text' - Get name suggestions\n"
    "  - random=True - Get random card\n"
    "  - collection=[identifiers] - Get multiple cards\n"
    "  - code='set', number='num' - Get by set and collector number\n"
    "  - multiverse='id' - Get by Multiverse ID\n"
    "  - mtgo='id' - Get by MTGO ID\n"
    "  - arena='id' - Get by Arena ID\n"
    "  - tcgplayer='id' - Get by TCGPlayer ID\n"
    "  - cardmarket='id' - Get by Cardmarket ID\n"
    "  - id='uuid' - Get by Scryfall ID\n"
    "See https://scryfall.com/docs/api/cards for details."
)
```

**Sets Factory** (`scrython/sets/sets.py`):

Note: Sets has a default (returns `AllSets()`), so no error needed. But add docstring:

```python
class Sets:
    """
    Factory class for accessing Scryfall sets endpoints.

    Examples:
        Get all sets:
            all_sets = scrython.Sets()

        Get specific set:
            set_obj = scrython.Sets(code='m21')
            set_obj = scrython.Sets(id='uuid-here')
            set_obj = scrython.Sets(tcgplayer_id=12345)
    """
    def __new__(self, **kwargs):
        # ... existing code
```

**BulkData Factory** (`scrython/bulk_data/bulk_data.py`):

Same as Sets - has default, add docstring:

```python
class BulkData:
    """
    Factory class for accessing Scryfall bulk data endpoints.

    Examples:
        Get all bulk data info:
            all_bulk = scrython.BulkData()

        Get specific bulk data:
            oracle_cards = scrython.BulkData(type='oracle_cards')
            specific = scrython.BulkData(id='uuid-here')
    """
    def __new__(self, **kwargs):
        # ... existing code
```

---

### Task 3.4: Add Caching Recommendations to README

Add new section to README.md:

```markdown
## Caching & Performance

### Cache Your Responses

Scryfall recommends caching API responses for at least 24 hours to reduce load on their servers.

**Simple Caching Example**:

```python
from functools import lru_cache
import scrython

@lru_cache(maxsize=1000)
def get_card_by_name(name: str):
    """Cache card lookups to avoid duplicate requests."""
    return scrython.Cards(fuzzy=name)

# First call makes API request
card1 = get_card_by_name('Lightning Bolt')

# Second call returns cached result (no API request)
card2 = get_card_by_name('Lightning Bolt')
```

### Use Bulk Data for Large Datasets

If you need to process thousands of cards, download bulk data instead:

```python
import scrython
import requests
import json

# Get bulk data download URL
bulk = scrython.BulkData(type='oracle_cards')
download_url = bulk.download_uri

# Download and process
response = requests.get(download_url)
cards = response.json()

# Now you have all cards locally - no rate limiting needed!
for card in cards:
    print(card['name'])
```

**Note**: Bulk data files are updated every 12 hours. Card prices become unreliable after 24 hours.
```

---

### Task 3.5: Update Tests for New Error Messages

**File**: `tests/test_cards.py`

**Update test** (around line 345):
```python
def test_factory_raises_error_no_mode(self):
    """Test that Cards factory raises error when no valid parameters provided."""
    with pytest.raises(ValueError, match='No valid parameters provided'):
        Cards()
```

**Run tests**:
```bash
pytest tests/test_cards.py::TestCardsFactory::test_factory_raises_error_no_mode -v
```

---

## Phase 4: Documentation & Type Hints (PARTIAL ✅)

**Status**: 🟡 PARTIAL COMPLETION - 40/149 properties documented
**Priority**: 🟡 MEDIUM - Greatly improves developer experience
**Estimated Time**: 8-12 hours (due to ~150 properties)
**Dependencies**: Phase 2 complete (Phase 3 recommended)
**Date Completed**: 2025-01-08 (Partial)

### Objectives:
Add comprehensive docstrings and type hints for better IDE support.

### What Was Completed:
- ✅ CoreFieldsMixin (17 properties) - All core card identifiers documented
- ✅ GameplayFieldsMixin (23 properties) - All gameplay mechanics documented
- ✅ Factory class docstrings (Cards, Sets, BulkData) - Completed in Phase 3

### What Remains (Optional Future Work):
- ⏸️ PrintFieldsMixin (48 properties) - Print-specific fields
- ⏸️ CardFaceMixin (23 properties) - Multi-face card properties
- ⏸️ RelatedCardsObjectMixin (6 properties) - Related card references
- ⏸️ SetsObjectMixin (21 properties) - Set metadata
- ⏸️ BulkDataObjectMixin (11 properties) - Bulk data metadata
- ⏸️ Type hints throughout codebase
- ⏸️ Additional README examples

**Assessment**: Library is ready for beta release with current documentation level.

---

### Task 4.1: Add Docstrings to Card Properties

**Files to Update**:
- `scrython/cards/cards_mixins.py`

**Process**:
1. Fetch official descriptions from Scryfall API docs
2. Add docstring to each `@property` with:
   - Official description from Scryfall
   - Type information
   - Nullability
   - Examples where helpful

**Format Template**:
```python
@property
def field_name(self):
    """
    [Official Scryfall description here - copy verbatim]

    Type: [String|Integer|Boolean|Array|Object|Decimal|UUID|URI|Date] (Nullable|Required)

    [Optional: Additional notes or examples]
    """
    return self.scryfall_data['field_name']
```

**Example - CoreFieldsMixin**:
```python
@property
def id(self):
    """
    A unique ID for this card in Scryfall's database.

    Type: UUID (Required)
    """
    return self.scryfall_data['id']

@property
def oracle_id(self):
    """
    A unique ID for this card's oracle identity. This value is consistent
    across reprinted card editions, and unique among different cards with
    the same name (tokens, Unstable variants, etc).

    Type: UUID (Nullable)

    Note: This field is null for cards that are not available in any language
    supported by Scryfall.
    """
    return self.scryfall_data['oracle_id']

@property
def multiverse_ids(self):
    """
    This card's multiverse IDs on Gatherer, if any. Note that Scryfall
    includes many promo cards, token cards, and non-English cards in this
    set which do not have these identifiers.

    Type: Array of Integers (Nullable)
    """
    return self.scryfall_data['multiverse_ids']
```

**Example - GameplayFieldsMixin**:
```python
@property
def mana_cost(self):
    """
    The mana cost for this card. This value will be any empty string ""
    if the cost is absent. Remember that per the game rules, a missing
    mana cost and a mana cost of {0} are different values.

    Type: String (Nullable)

    Example: "{3}{U}{U}"
    """
    return self.scryfall_data['mana_cost']

@property
def cmc(self):
    """
    The card's mana value (previously called "converted mana cost" or "CMC").
    If the card has {X} in a mana cost, X is treated as 0. If the card is
    split or double-faced, this value will be the sum of all faces.

    Type: Decimal (Required)
    """
    return self.scryfall_data['cmc']

@property
def type_line(self):
    """
    The type line of this card.

    Type: String (Required)

    Example: "Legendary Creature — Human Wizard"
    """
    return self.scryfall_data['type_line']
```

**Example - PrintFieldsMixin**:
```python
@property
def prices(self):
    """
    An object containing daily price information for this card, including
    usd, usd_foil, usd_etched, eur, eur_foil, and tix prices.

    Type: Object (Required)

    Note: Prices should be considered dangerously stale after 24 hours.

    Example:
        {
            "usd": "1.50",
            "usd_foil": "3.25",
            "usd_etched": null,
            "eur": "1.30",
            "eur_foil": null,
            "tix": "0.50"
        }
    """
    return self.scryfall_data['prices']
```

**Where to Find Descriptions**:
- https://scryfall.com/docs/api/cards
- Scroll to "Card Objects" section
- Copy descriptions verbatim for consistency

**Checklist**:
- [x] CoreFieldsMixin (17 properties) ✅
- [x] GameplayFieldsMixin (23 properties) ✅
- [ ] PrintFieldsMixin (48 properties) - DEFERRED
- [ ] CardFaceMixin (23 properties) - DEFERRED
- [ ] RelatedCardsObjectMixin (6 properties) - DEFERRED

**Total**: ~117 card-related properties
**Completed**: 40/117 (34%) - Sufficient for beta release

---

### Task 4.2: Add Docstrings to Set Properties

**File**: `scrython/sets/sets_mixins.py`

**Process**: Same as Task 4.1, using descriptions from https://scryfall.com/docs/api/sets

**Example**:
```python
@property
def code(self):
    """
    The unique three to five-letter code for this set.

    Type: String (Required)

    Example: "m21", "2xm", "plist"
    """
    return self.scryfall_data['code']

@property
def set_type(self):
    """
    A computer-readable classification for this set. See the Set Type
    documentation for more information.

    Type: String (Required)

    Examples: "core", "expansion", "masters", "draft_innovation"
    """
    return self.scryfall_data['set_type']

@property
def card_count(self):
    """
    The number of cards in this set.

    Type: Integer (Required)

    Note: This may include cards that are only available in the set's
    boosters and not in the set's main card list.
    """
    return self.scryfall_data['card_count']
```

**Checklist**:
- [ ] SetsObjectMixin (21 properties)

---

### Task 4.3: Add Docstrings to Bulk Data Properties

**File**: `scrython/bulk_data/bulk_data_mixins.py`

**Process**: Same as above, using https://scryfall.com/docs/api/bulk-data

**Example**:
```python
@property
def download_uri(self):
    """
    A URI that hosts this bulk file for fetching.

    Type: URI (Required)

    Note: Files are compressed with gzip. Download and decompress to process.
    """
    return self.scryfall_data['download_uri']

@property
def updated_at(self):
    """
    The time when this file was last updated.

    Type: Timestamp (Required)

    Note: Bulk data files are updated approximately every 12 hours.
    """
    return self.scryfall_data['updated_at']

@property
def size(self):
    """
    The size of this file in integer bytes.

    Type: Integer (Required)
    """
    return self.scryfall_data['size']
```

**Checklist**:
- [ ] BulkDataObjectMixin (11 properties)

---

### Task 4.4: Add Docstrings to Factory Classes

**Files**:
- `scrython/cards/cards.py` - Classes: CardsSearch, CardsNamed, etc., and Cards factory
- `scrython/sets/sets.py` - Classes: AllSets, SetsByCode, etc., and Sets factory
- `scrython/bulk_data/bulk_data.py` - Classes: AllBulkData, etc., and BulkData factory

**Format**:
```python
class CardsSearch(ScryfallListMixin, ScrythonRequestHandler):
    """
    Search for Magic cards using Scryfall's syntax.

    Endpoint: GET /cards/search

    Returns a list object containing Cards. The Cards object contains an array
    of the returned card objects in the data field.

    Args:
        q: A fulltext search query in Scryfall's syntax.
        unique: Strategy for omitting duplicate cards (optional).
            Options: 'cards', 'art', 'prints'
        order: Method to sort returned cards (optional).
            Options: 'name', 'set', 'released', 'rarity', 'color',
                    'usd', 'tix', 'eur', 'cmc', 'power', 'toughness',
                    'edhrec', 'penny', 'artist', 'review'
        dir: Direction to sort (optional). Options: 'auto', 'asc', 'desc'

    Example:
        # Search for red instants
        results = scrython.cards.CardsSearch(q='c:red type:instant')

        # Access results
        for card in results.data:
            print(card.name)

        # Check pagination
        if results.has_more:
            print(f"Total cards: {results.total_cards}")

    See: https://scryfall.com/docs/api/cards/search
    """
    _endpoint = '/cards/search'
    list_data_type = CardsObject
```

**Factory class example**:
```python
class Cards:
    """
    Smart factory for accessing all Scryfall card endpoints.

    This factory routes to the appropriate endpoint class based on the
    parameters provided. Use this instead of importing individual endpoint
    classes directly.

    Supported Modes:

        Named Lookup (fuzzy or exact match):
            card = Cards(fuzzy='Lightning Bolt')
            card = Cards(exact='Lightning Bolt')

        Search with Scryfall syntax:
            results = Cards(search='c:red cmc:1')

        Autocomplete:
            suggestions = Cards(autocomplete='light')

        Random card:
            card = Cards(random=True)

        Multiple cards by identifier:
            cards = Cards(collection=[
                {'name': 'Lightning Bolt'},
                {'id': 'card-uuid-here'}
            ])

        By set code and collector number:
            card = Cards(code='m21', number='123')
            card = Cards(code='m21', number='123', lang='ja')

        By various IDs:
            card = Cards(id='scryfall-uuid')
            card = Cards(multiverse='12345')
            card = Cards(mtgo='67890')
            card = Cards(arena='54321')
            card = Cards(tcgplayer='98765')
            card = Cards(cardmarket='11111')

    Returns:
        An instance of the appropriate endpoint class (CardsNamed,
        CardsSearch, etc.) based on the parameters provided.

    Raises:
        ValueError: If no valid parameters are provided.

    See: https://scryfall.com/docs/api/cards
    """
    def __new__(self, **kwargs):
        # ... existing routing logic
```

**Checklist**:
- [ ] All 12 Cards endpoint classes
- [ ] Cards factory class
- [ ] All 4 Sets endpoint classes
- [ ] Sets factory class
- [ ] All 3 BulkData endpoint classes
- [ ] BulkData factory class

**Total**: ~22 classes

---

### Task 4.5: Add Type Hints

**Files**: All Python files in `scrython/`

**Process**:
1. Add type hints to function signatures
2. Add type hints to class attributes
3. Import necessary types from `typing` module

**Example - base.py**:
```python
from typing import Dict, Any, Optional
import json
import urllib.error
import urllib.parse
from urllib.request import Request, urlopen

class ScryfallError(Exception):
    def __init__(self, scryfall_data: Dict[str, Any], *args: Any, **kwargs: Any) -> None:
        super(self.__class__, self).__init__(*args, **kwargs)

        self._status: int = scryfall_data['status']
        self._code: str = scryfall_data['code']
        self._details: str = scryfall_data['details']
        self._type: Optional[str] = scryfall_data['type']
        self._warnings: Optional[list] = scryfall_data['warnings']

    @property
    def status(self) -> int:
        return self._status

    # ... etc

class ScrythonRequestHandler:
    scryfall_data: Dict[str, Any] = {}
    _user_agent: str = 'Scrython/2.0 (https://github.com/NandaScott/Scrython)'
    _accept: str = 'application/json'
    _content_type: str = 'application/json'
    _endpoint: str = ''

    def __init__(self, **kwargs: Any) -> None:
        self._build_path(**kwargs)
        self._build_params(**kwargs)
        self._fetch(**kwargs)

        if self.scryfall_data['object'] == 'error':
            raise ScryfallError(self.scryfall_data, self.scryfall_data['details'])

    def _fetch(self, **kwargs: Any) -> None:
        # ... implementation

    def _build_params(self, **kwargs: Any) -> None:
        # ... implementation

    def _build_path(self, **kwargs: Any) -> None:
        # ... implementation
```

**Example - Mixins**:
```python
from typing import List, Dict, Any, Optional

class CoreFieldsMixin:
    scryfall_data: Dict[str, Any]

    @property
    def id(self) -> str:
        """A unique ID for this card in Scryfall's database."""
        return self.scryfall_data['id']

    @property
    def oracle_id(self) -> Optional[str]:
        """A unique ID for this card's oracle identity."""
        return self.scryfall_data.get('oracle_id')

    @property
    def multiverse_ids(self) -> Optional[List[int]]:
        """This card's multiverse IDs on Gatherer, if any."""
        return self.scryfall_data.get('multiverse_ids')
```

**Checklist**:
- [ ] base.py
- [ ] base_mixins.py
- [ ] cards/cards.py
- [ ] cards/cards_mixins.py
- [ ] sets/sets.py
- [ ] sets/sets_mixins.py
- [ ] bulk_data/bulk_data.py
- [ ] bulk_data/bulk_data_mixins.py
- [ ] utils.py

---

### Task 4.6: Update README with Complete Examples

Add comprehensive examples section to README.md showing:
- All factory patterns
- Common use cases
- Error handling
- Pagination
- Accessing nested data

**Example section to add**:

```markdown
## Complete Usage Examples

### Basic Card Lookup

```python
import scrython

# Fuzzy name search (handles typos)
card = scrython.Cards(fuzzy='Light Bolt')
print(card.name)  # "Lightning Bolt"
print(card.mana_cost)  # "{R}"
print(card.type_line)  # "Instant"

# Exact name match
card = scrython.Cards(exact='Black Lotus')
print(card.prices)
# {'usd': '25000.00', 'usd_foil': None, ...}
```

### Advanced Search

```python
# Search with Scryfall syntax
results = scrython.Cards(search='type:creature cmc:1 color:red')

print(f"Found {results.total_cards} cards")

for card in results.data:
    print(f"{card.name} - {card.set_name}")

# Handle pagination
if results.has_more:
    print("More results available - implement pagination as needed")
```

### Getting Specific Cards

```python
# By set code and collector number
card = scrython.Cards(code='znr', number='123')

# By various IDs
card = scrython.Cards(multiverse='456789')
card = scrython.Cards(mtgo='67890')
card = scrython.Cards(id='5f8287b1-5bb6-4e8f-9d78-8f3e3b3e1c6d')
```

### Working with Sets

```python
# Get all sets
all_sets = scrython.Sets()

for set_obj in all_sets.data:
    print(f"{set_obj.name} ({set_obj.code}) - {set_obj.card_count} cards")

# Get specific set
set_obj = scrython.Sets(code='znr')
print(f"{set_obj.name} released on {set_obj.released_at}")
```

### Bulk Data Download

```python
import scrython
import requests

# Get all bulk data options
all_bulk = scrython.BulkData()

for bulk in all_bulk.data:
    print(f"{bulk.name}: {bulk.description}")
    print(f"Size: {bulk.size / 1_000_000:.1f} MB")

# Download specific bulk data
oracle_cards = scrython.BulkData(type='oracle_cards')
print(f"Download from: {oracle_cards.download_uri}")

# Actually download (example)
response = requests.get(oracle_cards.download_uri)
cards = response.json()
print(f"Downloaded {len(cards)} cards")
```

### Error Handling

```python
from scrython.base import ScryfallError

try:
    card = scrython.Cards(exact='Nonexistent Card Name')
except ScryfallError as e:
    print(f"Error {e.status}: {e.details}")
    if e.warnings:
        print(f"Suggestions: {e.warnings}")
```

### Rate Limiting (Important!)

```python
import scrython
import time

card_names = ['Lightning Bolt', 'Counterspell', 'Dark Ritual']

for name in card_names:
    card = scrython.Cards(fuzzy=name)
    print(f"{card.name} - ${card.prices['usd']}")

    # REQUIRED: Add delay between requests
    time.sleep(0.1)  # 100ms = ~10 requests/second max
```
```

---

## Phase 5: Future Enhancements (Optional)

**Priority**: 🟢 LOW - Nice to have, not urgent
**Estimated Time**: Varies by feature

These are enhancements for future consideration, not required for v2.0 release.

---

### Enhancement 5.1: Implement Rulings API

**New files needed**:
- `scrython/rulings/rulings.py`
- `scrython/rulings/rulings_mixins.py`
- `tests/test_rulings.py`
- `tests/fixtures/rulings/*.json`

**Endpoints to implement** (5 total):
1. `/cards/multiverse/:id/rulings` → `RulingsByMultiverse`
2. `/cards/mtgo/:id/rulings` → `RulingsByMTGO`
3. `/cards/arena/:id/rulings` → `RulingsByArena`
4. `/cards/:code/:number/rulings` → `RulingsByCodeNumber`
5. `/cards/:id/rulings` → `RulingsById`

**Factory class**: `Rulings`

**Ruling object fields**:
- `object`: String - Always "ruling"
- `oracle_id`: UUID
- `source`: String - "wotc" or "scryfall"
- `published_at`: Date
- `comment`: String

**Integration**: Add to `scrython/__init__.py` exports

---

### Enhancement 5.2: Implement Catalogs API

**New files needed**:
- `scrython/catalog/catalog.py`
- `tests/test_catalog.py`
- `tests/fixtures/catalog/*.json`

**Endpoints to implement** (19 total):
All return catalog objects, so can use existing `ScryfallCatalogMixin`

1. `/catalog/card-names` → `CardNames`
2. `/catalog/artist-names` → `ArtistNames`
3. `/catalog/word-bank` → `WordBank`
4. ... (16 more type catalogs)

**Note**: These are simple GET endpoints with no parameters

**Integration**: Add to `scrython/__init__.py` exports

---

### Enhancement 5.3: Implement Symbology API

**New files needed**:
- `scrython/symbology/symbology.py`
- `scrython/symbology/symbology_mixins.py`
- `tests/test_symbology.py`
- `tests/fixtures/symbology/*.json`

**Endpoints to implement** (2 total):
1. `/symbology` → `AllSymbols`
2. `/symbology/parse-mana` → `ParseMana`

**Card Symbol object fields** (14 total):
- `object`, `symbol`, `loose_variant`, `english`, `transposable`
- `represents_mana`, `mana_value`, `appears_in_mana_costs`
- `funny`, `colors`, `hybrid`, `phyrexian`
- `gatherer_alternates`, `svg_uri`

**Integration**: Add to `scrython/__init__.py` exports

---

### Enhancement 5.4: Implement Card Migrations API (Beta)

**New files needed**:
- `scrython/migrations/migrations.py`
- `scrython/migrations/migrations_mixins.py`
- `tests/test_migrations.py`
- `tests/fixtures/migrations/*.json`

**Endpoints to implement** (2 total):
1. `/migrations` → `AllMigrations`
2. `/migrations/:id` → `MigrationById`

**Migration object fields** (9 total):
- `object`, `uri`, `id`, `performed_at`
- `migration_strategy`, `old_scryfall_id`, `new_scryfall_id`
- `note`, `metadata`

**Integration**: Add to `scrython/__init__.py` exports

---

### Enhancement 5.5: Add set_code Property Alias

**File**: `scrython/cards/cards_mixins.py`

**Rationale**: Avoid confusion with Python's built-in `set`

**Implementation**:
```python
class PrintFieldsMixin:
    # ... existing properties ...

    @property
    def set(self):
        """
        This card's set code.

        Type: String (Required)
        """
        return self.scryfall_data['set']

    @property
    def set_code(self):
        """
        Alias for `set` property. This card's set code.

        Type: String (Required)

        Note: This is an alias to avoid confusion with Python's built-in set().
        """
        return self.set
```

---

### Enhancement 5.6: Optional Rate Limiter Class

**New file**: `scrython/rate_limiter.py`

**Implementation idea**:
```python
import time
from datetime import datetime, timedelta

class RateLimiter:
    """
    Optional rate limiter for Scryfall API requests.

    Usage:
        limiter = scrython.RateLimiter(delay_ms=100)

        with limiter:
            card1 = scrython.Cards(fuzzy='Lightning Bolt')

        with limiter:
            card2 = scrython.Cards(fuzzy='Counterspell')
    """
    def __init__(self, delay_ms: int = 100):
        self.delay = delay_ms / 1000.0
        self.last_request = None

    def __enter__(self):
        if self.last_request:
            elapsed = (datetime.now() - self.last_request).total_seconds()
            if elapsed < self.delay:
                time.sleep(self.delay - elapsed)
        return self

    def __exit__(self, *args):
        self.last_request = datetime.now()
```

**Integration**: Optional, users can choose to use it or not

---

## Testing Strategy

### After Each Phase:

**Phase 2**: Run full test suite
```bash
source venv/bin/activate
pytest -v
# Expected: 84/84 passing
```

**Phase 3**: Run affected tests
```bash
pytest tests/test_cards.py::TestCardsFactory::test_factory_raises_error_no_mode -v
pytest tests/test_base.py -v
```

**Phase 4**: No test changes needed (docstrings/type hints don't affect behavior)
- But verify no syntax errors: `pytest --collect-only`

**Phase 5**: Write new tests for each new module
- Target: Same coverage as existing modules (>90%)

---

## Release Checklist

Before releasing Scrython 2.0:

- [ ] Phase 2 complete (critical bugs fixed)
- [ ] Phase 3 complete (API compliance)
- [ ] Phase 4 complete (documentation)
- [ ] All tests passing (84+)
- [ ] README updated with:
  - [ ] Rate limiting warnings
  - [ ] Complete examples
  - [ ] Caching recommendations
  - [ ] Custom User-Agent instructions
- [ ] CHANGELOG.md updated
- [ ] Version bumped in setup.py
- [ ] Documentation published (if applicable)

---

## Notes for Future Developers

### Working with This Plan

1. **Start at Phase 2** - The critical bugs must be fixed first
2. **Each phase is independent** - Can be done by different people
3. **Test after every change** - Don't accumulate untested changes
4. **Refer to ANALYSIS.md** - Has detailed rationale for all decisions
5. **Use API_CHECKLIST.md** - To track field implementation progress

### Code Style Guidelines

From `Contributing.md`:
- No single-character variables (except `f` for files, `i` for loops)
- 4 spaces indentation (no tabs)
- Complex code needs explanatory comments
- Weird/unexpected code needs "why" comments

### Important Context

- **No backwards compatibility promise** - Breaking changes are acceptable as Scryfall API evolves
- **Rate limiting is user responsibility** - Library doesn't enforce it
- **Python 3.8+ required** - Uses walrus operator (`:=`)
- **Main branch is `main`** - Not `master` (check repo for current default)

---

## Questions or Issues?

If something in this plan is unclear:

1. Check `ANALYSIS.md` for detailed rationale
2. Check `API_CHECKLIST.md` for field status
3. Refer to official Scryfall docs: https://scryfall.com/docs/api
4. Check existing test files for patterns
5. Open a GitHub issue for the project

---

## 🎉 Beta Release Readiness

**Scrython 2.0 is ready for beta release!**

### Completed Work (January 8, 2025):

**Phase 1: Analysis & Documentation** ✅
- Complete test suite (84/84 passing)
- Comprehensive API analysis
- Implementation roadmap

**Phase 2: Critical Bug Fixes** ✅
- Fixed 4 property name typos (mana_cost, prices, illustration_id)
- Fixed warnings() property consistency
- Added explicit urllib.error import

**Phase 3: API Compliance & Best Practices** ✅
- Added rate limiting documentation and warnings
- Improved User-Agent header with contact info
- Added set_user_agent() customization method
- Improved error messages with helpful parameter lists
- Added caching recommendations
- Factory class docstrings

**Phase 4: Documentation (Partial)** 🟡
- Documented 40/149 properties (27%)
- CoreFieldsMixin: All 17 properties documented
- GameplayFieldsMixin: All 23 properties documented
- Remaining 109 properties deferred to future releases

### What Works Now:
- ✅ All Cards API endpoints (12/12)
- ✅ All Sets API endpoints (4/4)
- ✅ All Bulk Data API endpoints (3/3)
- ✅ Factory pattern with intelligent routing
- ✅ Comprehensive error handling
- ✅ Mocked test suite (84 tests)
- ✅ Rate limiting guidance
- ✅ API compliance

### What's Next (Future Releases):
- Additional property docstrings (109 remaining)
- Type hints throughout codebase
- Rulings API (5 endpoints)
- Catalogs API (19 endpoints)
- Symbology API (2 endpoints)
- Card Migrations API (2 endpoints)

### Git Commits on `rewrite` branch:
1. `6f411b9` - Phase 1: Analysis & Documentation
2. `682402f` - Phase 2: Critical Bug Fixes
3. `6e6e0ac` - Phase 3: API Compliance & Best Practices
4. `0d0ceb4` - Phase 4 Part 1: Core and Gameplay docstrings

**Ready for**: Beta testing, community feedback, PyPI pre-release

---

**Last Updated**: 2025-01-08
**Plan Version**: 1.1
**Status**: ✅ READY FOR BETA RELEASE (Phases 1-3 complete, Phase 4 partial)
