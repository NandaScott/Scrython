"""
Property accessor mixins for tagger GraphQL API response data.

Provides TagObject (wrapper for individual tag/edge data) and
CardTagsMixin (property accessors for card tag responses).
"""

from typing import Any

from .tagger_types import TaggerCardData, TaggerEdgeData


class TagObject:
    """
    Wrapper for individual tag or edge data from the tagger GraphQL API.

    Similar to cards.Object, provides dot-notation access to tag fields
    and convenience methods.

    The Edge type has:
      - name: display name of the edge (the card/subject name)
      - subjectName: the card this edge is attached to
      - relatedName: the tag or relationship label

    TagObject.name returns relatedName (the actual tag label) for a more
    intuitive API. Use card_name for the subject card's name.

    Example:
        card_tags = scrython.tagger.CardTags(code="sos", number="170")
        for tag in card_tags.tags:
            print(f"{tag.name} ({tag.classifier})")
    """

    _data: TaggerEdgeData

    def __init__(self, data: TaggerEdgeData) -> None:
        self._data = data

    @property
    def name(self) -> str:
        """Tag name or relationship label.

        For Tagging edges, the tag name is nested in `tag.name`.
        Falls back to `relatedName`, then `name` (the edge display name).
        """
        tag_data = self._data.get("tag")
        if isinstance(tag_data, dict) and tag_data.get("name"):
            return tag_data["name"]
        related = self._data.get("relatedName")
        if related:
            return related
        return self._data["name"]

    @property
    def card_name(self) -> str:
        """The name of the card this edge belongs to (subjectName)."""
        return self._data.get("subjectName", self._data["name"])

    @property
    def classifier(self) -> str:
        """Edge classifier (ORACLE_CARD_TAG, PRINTING_TAG, SIMILAR_TO, etc.)."""
        return self._data["classifier"]

    @property
    def type(self) -> str:
        """Edge type: 'TAGGING' or 'RELATIONSHIP'."""
        return self._data["type"]

    @property
    def namespace(self) -> str | None:
        """Tag namespace (e.g., 'card', 'artwork', 'function', 'archetype')."""
        return self._data.get("namespace")

    @property
    def annotation(self) -> str | None:
        """Optional annotation/note on the edge."""
        return self._data.get("annotation")

    @property
    def metadata(self) -> str | None:
        """Optional metadata on the edge."""
        return self._data.get("metadata")

    @property
    def is_tag(self) -> bool:
        """True if this edge is a tag (TAGGING), not a relationship."""
        return self._data["type"] == "TAGGING"

    @property
    def is_relationship(self) -> bool:
        """True if this edge is a relationship, not a tag."""
        return self._data["type"] == "RELATIONSHIP"

    @property
    def is_oracle_tag(self) -> bool:
        """True if this is an Oracle card tag."""
        return self._data["classifier"] == "ORACLE_CARD_TAG"

    @property
    def is_printing_tag(self) -> bool:
        """True if this is a printing-specific tag."""
        return self._data["classifier"] == "PRINTING_TAG"

    @property
    def is_illustration_tag(self) -> bool:
        """True if this is an illustration tag."""
        return self._data["classifier"] == "ILLUSTRATION_TAG"

    def to_dict(self) -> dict[str, Any]:
        """Export tag data as a dictionary."""
        return dict(self._data)

    def __repr__(self) -> str:
        return (
            f"TagObject(name='{self.name}', " f"classifier='{self.classifier}', type='{self.type}')"
        )

    def __str__(self) -> str:
        return f"{self.name} ({self.classifier})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TagObject):
            return False
        return self.name == other.name and self.classifier == other.classifier

    def __hash__(self) -> int:
        return hash((self.name, self.classifier))


class CardTagsMixin:
    """
    Mixin providing property accessors for card tag query responses.

    Used by CardTags endpoint class to expose the card metadata and
    filtered tag lists after a GraphQL query.
    """

    _scryfall_data: dict[str, Any]
    _card_data: TaggerCardData | None = None
    _all_edges: list[TaggerEdgeData] = []
    _tags: list[TagObject] = []
    _relationships: list[TagObject] = []
    _oracle_tags: list[TagObject] = []
    _printing_tags: list[TagObject] = []
    _illustration_tags: list[TagObject] = []

    def _process_tags(self) -> None:
        """
        Process raw edge data into categorized TagObject lists.

        Called after _scryfall_data is populated from the GraphQL response.
        Separates edges into TAGGING vs RELATIONSHIP and further by classifier.
        """
        card_data = self._scryfall_data.get("cardBySet")
        if not card_data:
            return

        self._card_data = card_data
        raw_edges: list[dict[str, Any]] = card_data.get("edges", [])

        self._tags = []
        self._relationships = []
        self._oracle_tags = []
        self._printing_tags = []
        self._illustration_tags = []

        for edge in raw_edges:
            edge_obj = TagObject(edge)  # type: ignore[arg-type]
            if edge_obj.is_relationship:
                self._relationships.append(edge_obj)
            else:
                self._tags.append(edge_obj)
                if edge_obj.is_oracle_tag:
                    self._oracle_tags.append(edge_obj)
                elif edge_obj.is_printing_tag:
                    self._printing_tags.append(edge_obj)
                elif edge_obj.is_illustration_tag:
                    self._illustration_tags.append(edge_obj)

    @property
    def card_name(self) -> str | None:
        """The name of the card these tags belong to."""
        if self._card_data:
            return self._card_data.get("name")
        return None

    @property
    def oracle_id(self) -> str | None:
        """The oracle ID of the card."""
        if self._card_data:
            return self._card_data.get("oracleId")
        return None

    @property
    def printing_id(self) -> str | None:
        """The printing/Scryfall UUID of the card."""
        if self._card_data:
            return self._card_data.get("printingId")
        return None

    @property
    def illustration_id(self) -> str | None:
        """The illustration ID of this printing."""
        if self._card_data:
            return self._card_data.get("illustrationId")
        return None

    @property
    def card_id(self) -> str | None:
        """The Scryfall card UUID (same as printing_id)."""
        return self.printing_id

    @property
    def tags(self) -> list[TagObject]:
        """All tags on the card (excluding relationships)."""
        return self._tags

    @property
    def oracle_tags(self) -> list[TagObject]:
        """Oracle card tags (mechanical/functional tags)."""
        return self._oracle_tags

    @property
    def printing_tags(self) -> list[TagObject]:
        """Printing-specific tags."""
        return self._printing_tags

    @property
    def illustration_tags(self) -> list[TagObject]:
        """Artwork/illustration tags."""
        return self._illustration_tags

    @property
    def relationships(self) -> list[TagObject]:
        """Card relationships (similar to, better than, etc.)."""
        return self._relationships

    @property
    def tag_names(self) -> list[str]:
        """List of all tag names on this card."""
        return [t.name for t in self._tags]

    def has_tag(self, tag_name: str) -> bool:
        """
        Check if this card has a specific tag.

        Args:
            tag_name: The tag name to check (case-sensitive).

        Returns:
            True if the card has this tag.
        """
        return any(t.name == tag_name for t in self._tags)

    def tags_by_namespace(self, namespace: str) -> list[TagObject]:
        """
        Get all tags in a specific namespace/category.

        Args:
            namespace: The tag namespace (e.g., 'function', 'archetype').

        Returns:
            List of TagObject instances in that namespace.
        """
        return [t for t in self._tags if t.namespace == namespace]
