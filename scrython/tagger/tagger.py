"""
Endpoint classes for the Scryfall Tagger GraphQL API.

Provides high-level classes for querying card tags, browsing tags,
and searching by tag slugs. All classes use the shared TaggerSession
for GraphQL communication.
"""

from typing import Any

from ..rate_limiter import TaggerRateLimiter
from .tagger_graphql import TaggerSession
from .tagger_mixins import CardTagsMixin


class TaggerRequestHandler:
    """
    Base handler for tagger.scryfall.com GraphQL queries.

    Manages rate limiting and delegates GraphQL execution to TaggerSession.
    Follows a similar pattern to ScrythonRequestHandler but is intentionally
    separate since tagger uses GraphQL rather than REST endpoints.

    Endpoint classes should:
    1. Inherit from this class + appropriate mixins
    2. Set _rate_limiter_class (default: TaggerRateLimiter)
    3. Override _execute() to call TaggerSession.execute_graphql()
    """

    _rate_limiter_class: type[TaggerRateLimiter] = TaggerRateLimiter
    _override_limiter: TaggerRateLimiter | None = None
    _scryfall_data: dict[str, Any] = {}

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize a tagger request handler.

        Args:
            **kwargs: Endpoint-specific parameters, plus optional:
                - rate_limit (bool): Enable rate limiting (default: True)
                - rate_limit_per_second (float): Override rate limit
        """
        rate_limit_per_second = kwargs.get("rate_limit_per_second")
        if rate_limit_per_second is not None:
            self._override_limiter = TaggerRateLimiter(rate_limit_per_second)

        self._rate_limited = kwargs.get("rate_limit", True)

    def _wait_rate_limit(self) -> None:
        """Enforce rate limiting before executing a query."""
        if not self._rate_limited:
            return

        if self._override_limiter is not None:
            self._override_limiter.wait()
        else:
            self._rate_limiter_class.get_global_limiter().wait()

    def _execute(self, query: str, variables: dict[str, Any] | None = None) -> None:
        """
        Execute a GraphQL query and store the result.

        Args:
            query: GraphQL query string.
            variables: Query variables dictionary.
        """
        self._wait_rate_limit()
        self._scryfall_data = TaggerSession.execute_graphql(query, variables)

    @property
    def scryfall_data(self) -> dict[str, Any]:
        """Raw GraphQL response data dictionary."""
        return self._scryfall_data

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}()"


class CardTags(CardTagsMixin, TaggerRequestHandler):
    """
    Get all tags for a card by set code and collector number.

    Queries the tagger.scryfall.com GraphQL API using cardBySet
    and exposes tags, relationships, and card metadata through
    the CardTagsMixin property accessors.

    Args:
        code: The 3-5 letter set code (required, e.g., 'sos', 'lea').
        number: The collector number (required, e.g., '170', '1a').
        back: Whether to fetch the back face for double-faced cards
            (optional, default: False).

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

        self._execute(self._graphql_query, variables)
        self._process_tags()

    def __repr__(self) -> str:
        name = self.card_name or "Unknown"
        return f"CardTags(name='{name}')"

    def __str__(self) -> str:
        return f"Tags for {self.card_name or 'Unknown Card'}"


class TagSearch(TaggerRequestHandler):
    """
    Search or browse tags from the Scryfall Tagger.

    Queries the 'tags' field on the GraphQL API. Accepts search
    input for filtering by namespace, name pattern, etc.

    Args:
        input: Search input dict (optional). See tagger API for
            supported fields. When omitted, returns popular tags.

    Example:
        # Browse tags without filtering
        results = scrython.tagger.TagSearch()

        # Search for functional tags
        results = scrython.tagger.TagSearch(
            input={"namespace": "function"}
        )
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
        input_data = kwargs.pop("input", None)

        super().__init__(**kwargs)

        variables: dict[str, Any] = {}
        if input_data:
            variables["input"] = input_data

        self._execute(self._graphql_query, variables)

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

    Args:
        slug: The tag slug to look up (required).
        type: The TagType — one of 'ORACLE_CARD_TAG', 'PRINTING_TAG',
            or 'ILLUSTRATION_TAG' (required).

    Example:
        tag = scrython.tagger.TagBySlug(
            slug="removal", type="ORACLE_CARD_TAG"
        )
        print(tag.name, tag.description)
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
        slug = kwargs.pop("slug", None)
        tag_type = kwargs.pop("type", None)

        if not slug or not tag_type:
            raise ValueError("TagBySlug requires 'slug' and 'type' arguments")

        super().__init__(**kwargs)

        self._execute(
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
