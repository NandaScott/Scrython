"""
Endpoint classes for the Scryfall Tagger GraphQL API.

Provides high-level classes for querying card tags, browsing tags,
and searching by tag slugs. All classes use the shared TaggerSession
for GraphQL communication.

TaggerRequestHandler extends ScrythonRequestHandler to inherit
serialization (to_dict / to_json / from_dict), magic methods
(__repr__ / __str__ / __eq__ / __hash__), rate limiting, and
the global caching layer from the shared base.
"""

import hashlib
from typing import Any

from ..base import ScrythonRequestHandler
from ..cache import get_global_cache
from ..rate_limiter import TaggerRateLimiter
from .tagger_graphql import TaggerSession
from .tagger_mixins import CardTagsMixin


class TaggerRequestHandler(ScrythonRequestHandler):
    """
    Base handler for tagger.scryfall.com GraphQL queries.

    Extends ScrythonRequestHandler to inherit serialization
    (to_dict / to_json / from_dict), magic methods
    (__repr__ / __str__ / __eq__ / __hash__), and the shared
    namespace conversion (scryfall_data property).

    Does NOT call super().__init__() because GraphQL endpoints
    don't use REST URL path/param building. Rate limiting and
    caching are set up inline, and subclasses call
    _graphql_fetch(query, variables) to execute queries.

    Endpoint classes should:
    1. Inherit from this class + appropriate mixins
    2. Set _rate_limiter_class (default: TaggerRateLimiter)
    3. Call _graphql_fetch(query, variables) in __init__
    """

    _rate_limiter_class: Any = TaggerRateLimiter

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize a tagger request handler.

        Does NOT call super().__init__() because GraphQL endpoints
        don't use REST URL path/param building. Instead, sets up
        rate limiting and caching directly.

        Args:
            **kwargs: Endpoint-specific parameters, plus optional:
                - rate_limit (bool): Enable rate limiting (default: True)
                - rate_limit_per_second (float): Override rate limit
                - cache (bool): Enable caching (default: False)
                - cache_ttl (int): Cache TTL in seconds (default: 3600)
        """
        # Rate limiting setup (same pattern as ScrythonRequestHandler)
        rate_limit_per_second = kwargs.get("rate_limit_per_second")
        self._override_limiter: Any = None
        if rate_limit_per_second is not None:
            self._override_limiter = TaggerRateLimiter(rate_limit_per_second)

        self._rate_limited = kwargs.get("rate_limit", True)

        # Caching setup
        self._use_cache = kwargs.get("cache", False)
        self._cache_ttl = kwargs.get("cache_ttl", 3600)

        # Initialize data store
        self._scryfall_data: dict[str, Any] = {}

        # Note: super().__init__() is intentionally NOT called.
        # ScrythonRequestHandler.__init__() calls _build_path(),
        # _build_params(), and _fetch() which are REST-specific.
        # GraphQL endpoints set up their own query/variables and
        # call self._graphql_fetch(query, variables) explicitly.

    @staticmethod
    def _build_cache_key(query: str, variables: dict[str, Any]) -> str:
        """
        Generate a unique cache key from a GraphQL query and its variables.

        Produces a SHA256 hash of the query string and sorted variables,
        ensuring consistent keys for identical requests regardless of
        dictionary key ordering.

        Args:
            query: GraphQL query string.
            variables: Query variables dictionary.

        Returns:
            Hex string representing the cache key.
        """
        sorted_vars = sorted(variables.items())
        key_string = f"{query}||{sorted_vars}"
        return hashlib.sha256(key_string.encode()).hexdigest()

    def _graphql_fetch(self, query: str, variables: dict[str, Any] | None = None) -> None:
        """
        Execute a GraphQL query with rate limiting and caching.

        Handles rate limit enforcement, cache lookup, and delegates
        HTTP communication to TaggerSession. Called by subclasses
        after initialization.

        Args:
            query: GraphQL query string.
            variables: Query variables dictionary (optional).
        """
        variables = variables or {}

        # --- Rate limiting ---
        if self._rate_limited:
            limiter = self._override_limiter
            if limiter is not None:
                limiter.wait()
            else:
                self._rate_limiter_class.get_global_limiter().wait()

        # --- Caching ---
        if self._use_cache:
            cache_key = self._build_cache_key(query, variables)
            cache = get_global_cache()
            cached_data = cache.get(cache_key)
            if cached_data is not None:
                self._scryfall_data = cached_data
                # Invalidate namespace cache when data changes
                if hasattr(self, "_scryfall_namespace"):
                    delattr(self, "_scryfall_namespace")
                return

        # --- Execute GraphQL ---
        self._scryfall_data = TaggerSession.execute_graphql(query, variables)

        # --- Store in cache ---
        if self._use_cache:
            cache_key = self._build_cache_key(query, variables)
            cache = get_global_cache()
            cache.set(cache_key, self._scryfall_data, self._cache_ttl)

        # --- Invalidate namespace cache ---
        if hasattr(self, "_scryfall_namespace"):
            delattr(self, "_scryfall_namespace")

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}()"


class CardTags(CardTagsMixin, TaggerRequestHandler):
    """
    Get all tags for a card by set code and collector number.

    Queries the tagger.scryfall.com GraphQL API using cardBySet
    and exposes tags, relationships, and card metadata through
    the CardTagsMixin property accessors.

    Inherits serialization (to_dict / to_json / from_dict), magic
    methods (__eq__ / __hash__), and caching from the shared base.

    Args:
        code: The 3-5 letter set code (required, e.g., 'sos', 'lea').
        number: The collector number (required, e.g., '170', '1a').
        back: Whether to fetch the back face for double-faced cards
            (optional, default: False).
        cache (bool): Enable caching (default: False).
        cache_ttl (int): Cache TTL in seconds (default: 3600).
        rate_limit (bool): Enable rate limiting (default: True).
        rate_limit_per_second (float): Override rate limit.

    Example:
        # Get tags for Abigale, Poet Laureate
        tags = scrython.tagger.CardTags(code="sos", number="170")

        # Access all tags
        for tag in tags.tags:
            print(f"{tag.name} ({tag.classifier})")

        # Access specific tag types
        print(f"Oracle tags: {[t.name for t in tags.oracle_tags]}")
        print(f"Relationships: {[t.name for t in tags.relationships]}")

        # Check for specific tags
        if tags.has_tag("removal"):
            print("This card can remove things!")

        # Access card metadata
        print(f"Card: {tags.card_name}")
        print(f"Oracle ID: {tags.oracle_id}")

        # Export tag data
        tags_dict = tags.to_dict()
        tags_json = tags.to_json(indent=2)

        # Rehydrate without API call
        restored = scrython.tagger.CardTags.from_dict(tags_dict)
    """

    _graphql_query = """
    query($set: String!, $number: String!, $back: Boolean) {
      cardBySet(set: $set, number: $number, back: $back) {
        id
        name
        oracleId
        printingId
        illustrationId
        displayName
        edges {
          classifier
          type
          name
          relatedName
          subjectName
          namespace
          annotation
          metadata
          ... on Tagging {
            tag {
              name
              description
            }
          }
        }
      }
    }
    """

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize the CardTags query.

        Args:
            code: Set code (required).
            number: Collector number (required).
            back: Fetch back face for double-faced cards (optional).
            cache (bool): Enable caching (default: False).
            cache_ttl (int): Cache TTL in seconds (default: 3600).
            rate_limit (bool): Enable rate limiting (default: True).
            rate_limit_per_second (float): Override rate limit.
        """
        code = kwargs.pop("code", None)
        number = kwargs.pop("number", None)
        back = kwargs.pop("back", False)

        if not code or not number:
            raise ValueError("CardTags requires 'code' (set code) and 'number' (collector number)")

        super().__init__(**kwargs)

        variables: dict[str, Any] = {"set": str(code), "number": str(number)}
        if back:
            variables["back"] = back

        self._graphql_fetch(self._graphql_query, variables)
        self._process_tags()

    def __repr__(self) -> str:
        name = self.card_name or "Unknown"
        return f"CardTags(name='{name}')"

    def __str__(self) -> str:
        return f"Tags for {self.card_name or 'Unknown Card'}"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CardTags":
        """
        Construct a CardTags instance from a dictionary without an API call.

        Overrides ScrythonRequestHandler.from_dict() to also call
        _process_tags() so that tag property accessors work after rehydration.

        Args:
            data: Dictionary containing GraphQL response data
                  (typically the output of to_dict()).

        Returns:
            CardTags instance with tags processed and ready to use.
        """
        import copy

        instance = cls.__new__(cls)
        TaggerRequestHandler.__init__(instance)
        instance._scryfall_data = copy.deepcopy(data)
        instance._process_tags()
        return instance


class TagSearch(TaggerRequestHandler):
    """
    Search or browse tags from the Scryfall Tagger.

    Queries the 'tags' field on the GraphQL API. Accepts search
    input for filtering by namespace, name pattern, etc.

    Inherits serialization (to_dict / to_json / from_dict), magic
    methods (__eq__ / __hash__), and caching from the shared base.

    Args:
        input: Search input dict (optional). See tagger API for
            supported fields. When omitted, returns popular tags.
        cache (bool): Enable caching (default: False).
        cache_ttl (int): Cache TTL in seconds (default: 3600).
        rate_limit (bool): Enable rate limiting (default: True).
        rate_limit_per_second (float): Override rate limit.

    Example:
        # Browse tags without filtering
        results = scrython.tagger.TagSearch()

        # Search for functional tags
        results = scrython.tagger.TagSearch(
            input={"namespace": "function"}
        )

        # Export results
        results_dict = results.to_dict()
    """

    _graphql_query = """
    query($input: TagSearchInput) {
      tags(input: $input) {
        page
        perPage
        total
        results {
          ... on Tag {
            id
            name
            namespace
            description
            category
          }
        }
      }
    }
    """

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize the TagSearch query.

        Args:
            input: Search input dict (optional).
            cache (bool): Enable caching (default: False).
            cache_ttl (int): Cache TTL in seconds (default: 3600).
            rate_limit (bool): Enable rate limiting (default: True).
            rate_limit_per_second (float): Override rate limit.
        """
        input_data = kwargs.pop("input", None)

        super().__init__(**kwargs)

        variables: dict[str, Any] = {}
        if input_data:
            variables["input"] = input_data

        self._graphql_fetch(self._graphql_query, variables)

    @property
    def data(self) -> list[dict[str, Any]]:
        """Tag search results as a list of tag dicts."""
        tags_data = self._scryfall_data.get("tags", {})
        return tags_data.get("results", [])

    @property
    def total(self) -> int:
        """Total number of matching tags."""
        tags_data = self._scryfall_data.get("tags", {})
        return tags_data.get("total", 0)

    def __repr__(self) -> str:
        return f"TagSearch(total={self.total})"

    def __str__(self) -> str:
        return f"Tag search results ({self.total} tags)"


class TagBySlug(TaggerRequestHandler):
    """
    Look up a specific tag by its slug.

    Queries the 'tagBySlug' field on the GraphQL API.

    Inherits serialization (to_dict / to_json / from_dict), magic
    methods (__eq__ / __hash__), and caching from the shared base.

    Args:
        slug: The tag slug to look up (required).
        type: The TagType — one of 'ORACLE_CARD_TAG', 'PRINTING_TAG',
            or 'ILLUSTRATION_TAG' (required).
        cache (bool): Enable caching (default: False).
        cache_ttl (int): Cache TTL in seconds (default: 3600).
        rate_limit (bool): Enable rate limiting (default: True).
        rate_limit_per_second (float): Override rate limit.

    Example:
        tag = scrython.tagger.TagBySlug(
            slug="removal", type="ORACLE_CARD_TAG"
        )
        print(tag.name, tag.description)

        # Export tag data
        tag_dict = tag.to_dict()
    """

    _graphql_query = """
    query($slug: String!, $type: TagType!) {
      tagBySlug(slug: $slug, type: $type) {
        id
        name
        namespace
        description
        category
        aliases {
          name
        }
      }
    }
    """

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize the TagBySlug query.

        Args:
            slug: Tag slug (required).
            type: TagType string (required).
            cache (bool): Enable caching (default: False).
            cache_ttl (int): Cache TTL in seconds (default: 3600).
            rate_limit (bool): Enable rate limiting (default: True).
            rate_limit_per_second (float): Override rate limit.
        """
        slug = kwargs.pop("slug", None)
        tag_type = kwargs.pop("type", None)

        if not slug or not tag_type:
            raise ValueError("TagBySlug requires 'slug' and 'type' arguments")

        super().__init__(**kwargs)

        self._graphql_fetch(
            self._graphql_query,
            {"slug": str(slug), "type": str(tag_type)},
        )

    @property
    def tag_data(self) -> dict[str, Any]:
        """Raw tag data from the GraphQL response."""
        return self._scryfall_data.get("tagBySlug", {})

    @property
    def name(self) -> str:
        """Tag name."""
        return self.tag_data.get("name", "")

    @property
    def namespace(self) -> str | None:
        """Tag namespace."""
        return self.tag_data.get("namespace")

    @property
    def description(self) -> str | None:
        """Tag description."""
        return self.tag_data.get("description")

    @property
    def is_category(self) -> bool:
        """True if this tag is a category/container."""
        return self.tag_data.get("category", False)

    @property
    def aliases(self) -> list[str]:
        """List of alias tag names."""
        aliases_raw = self.tag_data.get("aliases", [])
        return [a.get("name", "") for a in aliases_raw if isinstance(a, dict)]

    def __repr__(self) -> str:
        return f"TagBySlug(name='{self.name}')"

    def __str__(self) -> str:
        desc = self.description or "No description"
        return f"{self.name}: {desc[:80]}"
