# Scrython API Wrapper - UX & Technical Analysis

**Date**: 2025-01-08
**Version Analyzed**: 2.0.0 (rewrite branch)
**Compared Against**: [Official Scryfall API Documentation](https://scryfall.com/docs/api)

---

## Executive Summary

This analysis compares the Scrython wrapper implementation against the official Scryfall API documentation and evaluates user experience, Pythonic conventions, and API compliance. Issues are categorized by severity, with specific recommendations for each.

**Overall Assessment**: ✅ Good architectural foundation with smart factory pattern, but contains critical bugs and missing Scryfall API requirements.

---

## Critical Issues (Must Fix)

### 1. Property Name Typos in `cards_mixins.py`
**Severity**: 🔴 Critical
**Impact**: Users cannot access essential card data; raises `KeyError`

**Issues Found**:
- Line 137: `mana_costmissing` should be `mana_cost`
- Line 411: `mana_costmana` should be `mana_cost` (in CardFaceMixin)
- Line 258: `pricesas` should be `prices`
- Line 242: `illustration_idfield` should be `illustration_id`

**Example User Impact**:
```python
card = scrython.Cards(fuzzy="Black Lotus")
print(card.mana_cost)  # KeyError: 'mana_costmissing'
print(card.prices)     # KeyError: 'pricesas'
```

**Recommendation**: Fix typos immediately. These are copy-paste errors that break core functionality.

---

### 2. Missing Rate Limiting (API Requirement Violation)
**Severity**: 🔴 Critical
**Impact**: Risk of IP bans from Scryfall

**Scryfall Requirement**:
> "Please insert 50–100 milliseconds of delay between requests" (~10 requests/second)
>
> "Posting excessive requests is grounds for a temporary or permanent ban from our service."

**Current Implementation**: ❌ No rate limiting, no warnings in documentation

**Recommendation**:
1. Add prominent warning in README about rate limits
2. Consider implementing optional rate limiting in base class
3. Document that users are responsible for implementing delays

---

### 3. Missing `self` Parameter Bug (Already Fixed in Tests)
**Severity**: 🔴 Critical (FIXED)
**Location**: `scrython/sets/sets_mixins.py` (fixed during test implementation)

**Was**: All properties missing `self` parameter
**Status**: ✅ Fixed during test suite creation

---

## High Priority Issues

### 4. User-Agent Header Not Following API Guidelines
**Severity**: 🟠 High
**Impact**: Not following Scryfall best practices

**Scryfall Requirement**:
> "Both the User-Agent and Accept headers are required in every API request. The User-Agent header should accurately describe your application, its version number, and how you can be contacted."

**Current Implementation**:
```python
_user_agent = 'Scrython/2.0'  # base.py:36
```

**Issues**:
- Hardcoded version number (won't update)
- No contact information
- Doesn't encourage users to set their own User-Agent

**Recommendation**:
1. Allow users to configure User-Agent via environment variable or parameter
2. Update default to include contact: `Scrython/2.0 (https://github.com/NandaScott/Scrython)`
3. Add to README: "Please set a custom User-Agent for your application"

---

### 5. Factory Error Messages Not Helpful
**Severity**: 🟠 High
**Impact**: Poor developer experience

**Current Behavior**:
```python
scrython.Cards()  # Exception: No mode found
```

**Problem**: Doesn't tell users what parameters are valid

**Recommendation**:
```python
raise ValueError(
    "No valid parameters provided to Cards factory. "
    "Use one of: fuzzy='name', exact='name', search='query', "
    "autocomplete='text', random=True, collection=[...], "
    "code='set' and number='num', multiverse='id', mtgo='id', "
    "arena='id', tcgplayer='id', cardmarket='id', or id='uuid'"
)
```

---

### 6. Property Naming Conflicts with Python Built-ins
**Severity**: 🟠 High
**Impact**: Shadows Python's `set` built-in

**Issue**:
```python
# PrintFieldsMixin line 322
@property
def set(self):
    return self.scryfall_data['set']
```

**Problem**: `set` shadows Python's built-in `set()` type, which can cause confusion

**User Impact**:
```python
card = scrython.Cards(fuzzy="Lightning Bolt")
my_set = set([1, 2, 3])  # Fine, set() is available
card_set = card.set      # Fine, but confusing naming
```

**Recommendation**:
- Keep `set` for backward compatibility (matches Scryfall API)
- Add alias `set_code` as more Pythonic alternative
- Document this in README

---

## Medium Priority Issues

### 7. No Caching Recommendations
**Severity**: 🟡 Medium
**Impact**: Users may over-request data

**Scryfall Recommendation**:
> "Please cache responses for at least 24 hours locally"

**Current**: No documentation or guidance about caching

**Recommendation**: Add to README:
- Encourage local caching of card data (24+ hours)
- Suggest using bulk data downloads for large datasets
- Provide example of simple caching decorator

---

### 8. No Type Hints
**Severity**: 🟡 Medium
**Impact**: Reduced IDE autocomplete, no static type checking

**Current**: No type annotations anywhere

**Example Enhancement**:
```python
from typing import Dict, Any, Optional

class ScrythonRequestHandler:
    scryfall_data: Dict[str, Any] = {}

    def __init__(self, **kwargs: Any) -> None:
        ...

    def _build_path(self, **kwargs: Any) -> None:
        ...
```

**Recommendation**: Phase 4 enhancement, not urgent but improves DX

---

### 9. Missing Docstrings
**Severity**: 🟡 Medium
**Impact**: Poor IDE experience, unclear usage

**Current**: No docstrings on public classes/methods/properties

**Recommendation**:
```python
class Cards:
    """
    Factory class for accessing Scryfall card endpoints.

    Examples:
        Search for cards:
            results = Cards(search='c:red power>5')

        Get specific card:
            card = Cards(fuzzy='Black Lotus')
            card = Cards(exact='Lightning Bolt')

        Random card:
            card = Cards(random=True)
    """

# Example property docstrings using official API descriptions:
class GameplayFieldsMixin:
    @property
    def mana_cost(self):
        """
        The mana cost for this card. This value will be any empty string ""
        if the cost is absent. Remember that per the game rules, a missing
        mana cost and a mana cost of {0} are different values.

        Type: String (Nullable)
        """
        return self.scryfall_data['mana_cost']

    @property
    def cmc(self):
        """
        The card's mana value (previously called "converted mana cost"). If
        the card has multiple parts, this value will be the sum of all parts.

        Type: Decimal
        """
        return self.scryfall_data['cmc']
```

**Implementation Plan**:
- Copy official descriptions from Scryfall API docs for all ~150+ properties
- Maintain consistency with API terminology
- Include type information and nullability
- Add examples for complex fields

---

### 10. Optional Path Parameters Not Fully Implemented
**Severity**: 🟡 Medium
**Impact**: Language parameter (`:lang?`) doesn't work as expected

**Issue**: Optional parameters marked with `?` are stripped from path but not used in query params

**Current in `base.py` lines 94-102**:
```python
if optional:
    key = key[:-1]

value = kwargs.get(key, None)
if value is None and not optional:
    raise KeyError(f"Missing required path parameter: '{key}'")

if value is not None and not optional:
    resolved.append(str(value))
```

**Problem**: Optional params like `:lang?` in `/cards/:code/:number/:lang?` are removed from path but never added back

**Recommendation**: Clarify whether optional path params should go in path or query string per Scryfall API

---

## Low Priority / Informational

### 11. Inconsistent Import Structure
**Severity**: 🟢 Low
**Impact**: Minor, mostly aesthetic

**Issue**: Mixed import styles
```python
# Some files use relative imports
from .cards_mixins import CoreFieldsMixin
# Others use absolute
from scrython.base import ScrythonRequestHandler
```

**Recommendation**: Standardize on one style (relative imports preferred within package)

---

### 12. Unused urllib Error Import
**Severity**: 🟢 Low
**Impact**: None, just code cleanliness

**In `base.py` line 68**:
```python
except urllib.error.HTTPError as exc:
    raise Exception(f'{exc}: {request.get_full_url()}')
```

**Issue**:
- Catches `urllib.error.HTTPError` but `urllib.error` is never imported
- Should import: `import urllib.error`
- Actually works because full path is used, but unconventional

---

## API Coverage Comparison

### ✅ Fully Implemented Endpoints

**Cards** (12/12 endpoints):
- ✅ `/cards/search` → `CardsSearch`
- ✅ `/cards/named` → `CardsNamed`
- ✅ `/cards/autocomplete` → `CardsAutocomplete`
- ✅ `/cards/random` → `CardsRandom`
- ✅ `/cards/collection` → `CardsCollection`
- ✅ `/cards/:code/:number(/:lang)` → `CardsByCodeNumber`
- ✅ `/cards/multiverse/:id` → `CardsByMultiverseId`
- ✅ `/cards/mtgo/:id` → `CardsByMTGOId`
- ✅ `/cards/arena/:id` → `CardsByArenaId`
- ✅ `/cards/tcgplayer/:id` → `CardsByTCGPlayerId`
- ✅ `/cards/cardmarket/:id` → `CardsByCardMarketId`
- ✅ `/cards/:id` → `CardsById`

**Sets** (4/4 endpoints):
- ✅ `/sets` → `AllSets`
- ✅ `/sets/:code` → `SetsByCode`
- ✅ `/sets/tcgplayer/:id` → `SetsByTCGPlayerId`
- ✅ `/sets/:id` → `SetsById`

**Bulk Data** (3/3 endpoints):
- ✅ `/bulk-data` → `AllBulkData`
- ✅ `/bulk-data/:id` → `BulkDataById`
- ✅ `/bulk-data/:type` → `BulkDataByType`

### ❌ Missing Modules (Referenced in setup.py but not implemented)

**From setup.py line 5**:
```python
packages=['scrython', 'scrython.cards', 'scrython.rulings',
          'scrython.catalog', 'scrython.sets', 'scrython.symbology',
          'scrython.bulk_data']
```

**Not Yet Implemented**:
- ❌ Rulings API
- ❌ Catalog API
- ❌ Symbology API

**Status**: These were removed from setup.py during test suite creation (Phase 0)

---

## Error Handling Comparison

### ✅ Matches Scryfall Error Format

**Scryfall Error Object**:
```json
{
  "object": "error",
  "status": 404,
  "code": "not_found",
  "details": "No card found with the given ID",
  "type": "ambiguous",
  "warnings": ["Did you mean 'Lightning Bolt'?"]
}
```

**Scrython Implementation** (`base.py` lines 5-32):
```python
class ScryfallError(Exception):
    def __init__(self, scryfall_data, *args, **kwargs):
        self._status = scryfall_data['status']
        self._code = scryfall_data['code']
        self._details = scryfall_data['details']
        self._type = scryfall_data['type']
        self._warnings = scryfall_data['warnings']
```

**Assessment**: ✅ Perfect match with Scryfall's error structure

**Minor Issue**: `warnings()` should be a property, not a method (inconsistent with other accessors)

---

## Architectural Strengths

### ✅ Smart Factory Pattern
The use of `__new__()` to route to appropriate endpoint classes is elegant:

```python
class Cards:
    def __new__(self, **kwargs):
        if search := kwargs.get('search', None):
            return CardsSearch(q=search, **kwargs)
        if kwargs.get('fuzzy', None):
            return CardsNamed(**kwargs)
        # ... etc
```

**Benefits**:
- Single entry point for all card operations
- Intuitive parameter-based routing
- Pythonic use of walrus operator (`:=`)

### ✅ Clean Mixin Architecture
Separation of concerns through mixins is well-designed:

- `CoreFieldsMixin` - IDs and core metadata
- `GameplayFieldsMixin` - Game mechanics data
- `PrintFieldsMixin` - Printing-specific details
- `ScryfallListMixin` - Paginated list handling
- `ScryfallCatalogMixin` - Catalog response handling

### ✅ DRY Request Handling
`ScrythonRequestHandler` base class eliminates code duplication:
- Centralized path building with parameter substitution
- Unified query parameter handling
- Single HTTP request implementation

---

## Recommendations Summary

### Immediate (Phase 2 - Critical Bugs):
1. ✅ Fix property typos in `cards_mixins.py`
2. Fix `warnings()` to be property not method
3. Import `urllib.error` explicitly

### Short Term (Phase 3 - API Compliance):
1. Add rate limiting documentation to README
2. Update User-Agent header with contact info
3. Allow custom User-Agent configuration
4. Improve factory error messages
5. Add caching recommendations to docs

### Long Term (Phase 4 - UX Enhancements):
1. Add official API docstrings to all properties (~150+ properties across all mixins)
2. Add docstrings to factory classes and endpoints
3. Add type hints throughout
4. Consider adding `set_code` alias
5. Standardize import style
6. Consider implementing optional rate limiter class

---

## Test Coverage Status

**Current**: 84/84 tests passing ✅

**Coverage by Module**:
- ✅ Base classes (17 tests)
- ✅ Cards endpoints (40 tests)
- ✅ Sets endpoints (14 tests)
- ✅ Bulk Data endpoints (13 tests)

**Testing Infrastructure**:
- ✅ Mocked HTTP responses (no real API calls)
- ✅ Fixture-based test data
- ✅ Comprehensive factory routing tests
- ✅ Mixin property tests

---

## Conclusion

Scrython's rewrite shows excellent architectural decisions (factory pattern, mixins, DRY principles) but has critical bugs that must be fixed before release. The wrapper fully covers all documented Scryfall endpoints for Cards, Sets, and Bulk Data.

**Priority Actions**:
1. Fix property name typos (blocks core functionality)
2. Add rate limiting warnings (avoids API bans)
3. Improve error messages (better DX)
4. Add missing documentation (caching, User-Agent)

Once these are addressed, Scrython 2.0 will provide an excellent Pythonic interface to the Scryfall API.
