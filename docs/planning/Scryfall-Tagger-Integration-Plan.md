# Scryfall Tagger Integration Plan for Scrython

## 0. Discovery Results (COMPLETE)

### Confirmed Architecture

- **Base URL**: `https://tagger.scryfall.com`
- **API Type**: GraphQL (not REST, not HTML scraping)
- **Endpoint**: `POST /graphql` with JSON body `{"query": "...", "variables": {...}}`
- **Content-Type**: `application/json`

### Authentication Model

Tagger uses **session cookie + CSRF token** (Rails-style):

1. **GET** any HTML page (e.g., `/card/sos/170`) → receives `_scryfall_tagger_session` cookie
2. Extract CSRF token from `<meta name="csrf-token" content="...">`
3. **POST** to `/graphql` with `X-CSRF-Token` header + session cookie

This means `TaggerRequestHandler` must:

- Use a **persistent `http.cookiejar.CookieJar`** with a shared opener
- Automatically fetch a fresh CSRF token when needed
- Handle CSRF token expiry (new token per session)

### GraphQL Schema (key types)

**Query root fields** (relevant to MVP):

| Field | Args | Returns | Description |
|---|---|---|---|
| `card` | `id: ID!, back: Boolean` | `Card` | Lookup by Scryfall printing UUID |
| `cardBySet` | `set: String!, number: String!, back: Boolean` | `Card` | **PRIMARY: lookup by set+collector number** |
| `cards` | `input: CardSearchInput` | `CardSearchResults` | Search cards (paginated) |
| `tag` | `id: ID!` | `Tag` | Lookup tag by ID |
| `tagBySlug` | `slug: String!, type: TagType!` | `Tag` | Lookup tag by slug |
| `tags` | `input: TagSearchInput` | `TagSearchResults` | Search/browse tags (paginated) |
| `edges` | `input: EdgeSearchInput` | `EdgeSearchResults` | Search edges (taggings + relationships) |
| `sampleTags` | `count: Int!` | `[Tag]` | Random tag samples |
| `suggest` | `input: SuggestionInput` | `[Suggestion]` | Autocomplete suggestions |

**Card type** (`object`, not interface):

- `id: ID` — Scryfall printing UUID
- `oracleId: ID`
- `printingId: ID`
- `illustrationId: ID`
- `name: String`, `displayName: String`, `artist: String`
- `collectorNumber: String`
- `edges: [Edge]` — **tags + relationships live here**
- `relationships(moderatorView): [Relationship]`

**Edge interface** (base for Tagging and Relationship):

- `classifier: EdgeClassifier` — `ORACLE_CARD_TAG`, `PRINTING_TAG`, `ILLUSTRATION_TAG`, or relationship classifiers
- `type: EdgeType` — `TAGGING` or `RELATIONSHIP`
- `name: String` — tag name or relationship label
- `card: Card`
- `namespace: String`
- `annotation: String`, `metadata: String`

**Tag type**:

- `id: ID`, `name: String`, `namespace: String`
- `description: String`
- `category: Boolean` — whether this tag is a category (parent)
- `aliases: [Tag]`, `ancestorTags: [Tag]`, `descendants: [Tag]`
- `childTags: [Tag]`, `parentTags: [Tag]`
- `hierarchy: [TagHierarchy]`

**Enum `EdgeClassifier`**: `ILLUSTRATION_TAG`, `ORACLE_CARD_TAG`, `PRINTING_TAG`, `BETTER_THAN`, `COLORSHIFTED`, `COMES_AFTER`, `COMES_BEFORE`, `DEPICTED_IN`, `DEPICTS`, `MIRRORS`, `REFERENCED_BY`, `REFERENCES_TO`, `RELATED_TO`, `SIMILAR_TO`, `WITH_BODY`, `WITHOUT_BODY`, `WORSE_THAN`

**Enum `TagType`**: `ILLUSTRATION_TAG`, `ORACLE_CARD_TAG`, `PRINTING_TAG`

### Card Tags Retrieval Pattern

To get tags for a card by set code + collector number:

```graphql
query($set: String!, $number: String!) {
  cardBySet(set: $set, number: $number) {
    name
    edges {
      classifier
      type
      name
      namespace
      annotation
    }
  }
}
```

Filter edges where `type == "TAGGING"` and `classifier == "ORACLE_CARD_TAG"` (or `PRINTING_TAG`, `ILLUSTRATION_TAG`).

---

## 1. Module Structure

```
scrython/
├── tagger/                    # NEW subpackage
│   ├── __init__.py           # Public API: CardTags, TagSearch, TagObject, etc.
│   ├── tagger.py             # Endpoint classes inheriting TaggerRequestHandler
│   ├── tagger_mixins.py      # Property accessors for Tag objects
│   ├── tagger_types.py       # TypedDicts
│   └── tagger_graphql.py     # GraphQL client (session, CSRF, query execution)
```

---

## 2. `TaggerRequestHandler` — Base Class Design

**Key differences** from `ScrythonRequestHandler`:

1. Different base URL (`tagger.scryfall.com` vs `api.scryfall.com`)
2. GraphQL POST requests (not GET with query params)
3. Session + CSRF token management
4. Response parsing: GraphQL `{"data": {...}}` wrapper vs REST JSON

**Design**:

```python
class TaggerRequestHandler:
    """Base handler for tagger.scryfall.com GraphQL API."""
    
    _base_url = "https://tagger.scryfall.com"
    _graphql_endpoint = "/graphql"
    _rate_limiter_class = TaggerRateLimiter
    
    # Session state (shared across instances via class-level opener?)
    _cookie_jar: http.cookiejar.CookieJar
    _opener: urllib.request.OpenerDirector
    _csrf_token: str | None
    
    def _ensure_session(self) -> None:
        """GET HTML page to obtain session cookie + CSRF token."""
        
    def _execute_graphql(self, query: str, variables: dict) -> dict:
        """POST GraphQL query, return data dict."""
        
    def _fetch(self, **kwargs) -> None:
        """Build and execute GraphQL query, populate _scryfall_data."""
```

Because session management is cross-instance (same CSRF token for all requests in a session), this should use class-level state or a shared session manager. The rate limiter and caching still work per-instance.

---

## 3. Rate Limiter

```python
class TaggerRateLimiter(RateLimiter):
    def __init__(self, calls_per_second: float = 5.0) -> None:
        super().__init__(calls_per_second)
```

Conservative 5 req/s default. Tagger is a community-run project.

---

## 4. MVP Endpoints

### 4a. `CardTags` — PRIMARY (P0)

```python
class CardTags(TaggerRequestHandler):
    """Get all tags for a card by set code and collector number.
    
    Queries the tagger GraphQL API: cardBySet(set, number) { edges }
    Filters edges by type=TAGGING to return only tags.
    """
    _query = """
    query($set: String!, $number: String!) {
      cardBySet(set: $set, number: $number) {
        id, name, oracleId, printingId, illustrationId,
        edges {
          classifier, type, name, namespace, annotation, metadata
        }
      }
    }
    """
```

**Usage**:

```python
tags = scrython.tagger.CardTags(code="sos", number="170")
for tag in tags.data:
    print(f"{tag.name} ({tag.classifier})")
# Access card info: tags.card_name, tags.oracle_id
```

### 4b. `TagSearch` — P1

Search/browse tags by namespace, name pattern, etc. Uses `tags(input: TagSearchInput)` GraphQL query. Returns paginated `TagSearchResults`.

### 4c. `TagBySlug` — P1

Look up a specific tag by slug. Uses `tagBySlug(slug, type)` query.

### 4d. `TagObject` — P1

Wrapper for individual Tag/Edge data, following `cards.Object` pattern.

---

## 5. Type Definitions (`tagger_types.py`)

```python
class TaggerCardData(TypedDict):
    """Card data from tagger GraphQL."""
    id: str
    name: str
    oracleId: str
    printingId: str
    illustrationId: str

class TaggerEdgeData(TypedDict):
    """Edge data (tag or relationship) from tagger GraphQL."""
    classifier: str       # ILLUSTRATION_TAG, ORACLE_CARD_TAG, PRINTING_TAG, etc.
    type: str             # TAGGING or RELATIONSHIP
    name: str             # Tag name or relationship label
    namespace: NotRequired[str]
    annotation: NotRequired[str]
    metadata: NotRequired[str]

class TaggerTagData(TypedDict):
    """Tag type data from tagger GraphQL."""
    id: str
    name: str
    namespace: str
    description: NotRequired[str]
    category: bool        # True if this is a tag category
```

---

## 6. Session Management Strategy

The key challenge is that GraphQL requires CSRF + session cookie. Options:

| Approach | Pros | Cons |
|---|---|---|
| **A: Class-level shared session** | Simple, one opener for all instances | Not thread-safe without locks |
| **B: Per-instance session** | Thread-safe | Each instance makes extra GET request |
| **C: `TaggerSession` context manager** | Explicit lifecycle, testable | Different API from other Scrython classes |

**Recommendation: Option A** — Class-level shared opener with a threading lock for CSRF refresh. The `_ensure_session()` method checks if the session is valid and refreshes the CSRF token as needed. This is efficient (one HTML GET per session, not per request) and follows the "behind-the-scenes" philosophy of Scrython.

---

## 7. Implementation Order

| Step | Files | Effort |
|---|---|---|
| **1. Create `tagger_graphql.py`** | GraphQL client with session+CSRF management | Medium |
| **2. Create `TaggerRateLimiter`** | Subclass of `RateLimiter` with 5 req/s default | Small |
| **3. Create `tagger_types.py`** | TypedDict definitions | Small |
| **4. Create `tagger.py`** | `CardTags`, `TagSearch`, `TagBySlug` endpoint classes | Medium |
| **5. Create `tagger_mixins.py`** | `TagObject` wrapper + property accessors | Medium |
| **6. Create `tagger/__init__.py`** | Public API exports | Small |
| **7. Create `tests/test_tagger.py` + fixtures** | Mock GraphQL responses | Medium |
| **8. Wire up `scrython/__init__.py`** | Add `tagger` to exports | Small |
| **9. Run full test suite** | Ensure 394+ existing tests pass | Small |
| **10. Update `CHANGELOG.md`** | Document new module | Small |

---

## 8. Discovery Scripts (artifacts)

All discovery scripts are preserved in `Scrython/scripts/`:

- `discover_tagger.py` — Initial REST/JSON probing
- `discover_tagger_deep.py` — JS bundle analysis, API path probing
- `probe_graphql.py` — Initial GraphQL attempts (failed: CSRF)
- `probe_graphql_csrf.py` — CSRF token extraction
- `probe_graphql_session.py` — Session-based GraphQL (success!)
- `introspect_graphql.py` — Full schema introspection (complete)

---

## 9. Key Design Decisions

| Decision | Rationale |
|---|---|
| GraphQL POST (not REST GET) | Tagger uses GraphQL exclusively; no REST API exists |
| Session + CSRF auth | Required by Rails backend; transparent to end users |
| Class-level shared session | Efficient; matches Scrython's "it just works" philosophy |
| urllib + stdlib only | Zero external dependencies, consistent with Scrython |
| Filter edges by `classifier` | Tags and relationships share the `edges` field; must distinguish |
| `TaggerRateLimiter` at 5 req/s | Conservative for community-run service |
