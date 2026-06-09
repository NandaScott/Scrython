from typing import Any

from ..types import ScryfallTagData, ScryfallTaggingData
from ..utils import to_object_array


class TaggingObjectMixin:
    """Provides property accessors for tagging objects nested in a Tag."""

    _scryfall_data: ScryfallTaggingData

    @property
    def object(self) -> str:
        """
        A content type for this object, always "tagging".

        Type: String (Required)
        """
        return "tagging"

    @property
    def weight(self) -> str:
        """
        How strongly this tagging applies. One of "very_strong", "strong",
        "median", or "weak".

        Type: String (Required)
        """
        return self._scryfall_data["weight"]

    @property
    def illustration_id(self) -> str | None:
        """
        The illustration this tagging applies to, present on art taggings.

        Type: UUID (Nullable)
        """
        return self._scryfall_data.get("illustration_id")

    @property
    def oracle_id(self) -> str | None:
        """
        The Oracle identity this tagging applies to, present on oracle taggings.

        Type: UUID (Nullable)
        """
        return self._scryfall_data.get("oracle_id")

    @property
    def annotation(self) -> str | None:
        """
        A human-readable note describing why the tag applies.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("annotation")


class TagObjectMixin:
    """Provides property accessors for tag objects from the Scryfall bulk files."""

    _scryfall_data: ScryfallTagData

    @property
    def object(self) -> str:
        """
        A content type for this object, always "tag".

        Type: String (Required)
        """
        return "tag"

    @property
    def id(self) -> str:
        """
        A stable, unique identifier for this tag.

        Type: UUID (Required)
        """
        return self._scryfall_data["id"]

    @property
    def slug(self) -> str:
        """
        The URL-safe identifier for this tag.

        Type: String (Required)
        """
        return self._scryfall_data["slug"]

    @property
    def label(self) -> str:
        """
        The human-readable name of this tag.

        Type: String (Required)
        """
        return self._scryfall_data["label"]

    @property
    def uri(self) -> str:
        """
        A link to a Scryfall search for cards carrying this tag.

        Type: URI (Required)
        """
        return self._scryfall_data["uri"]

    @property
    def type(self) -> str:
        """
        The kind of tag. Either "illustration" (art tag) or "oracle".

        Type: String (Required)
        """
        return self._scryfall_data["type"]

    @property
    def description(self) -> str | None:
        """
        A description of what this tag represents.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("description")

    @property
    def parent_ids(self) -> list[str] | None:
        """
        The IDs of tags this tag is a child of.

        Type: Array of UUIDs (Nullable)
        """
        return self._scryfall_data.get("parent_ids")

    @property
    def child_ids(self) -> list[str] | None:
        """
        The IDs of tags that are children of this tag.

        Type: Array of UUIDs (Nullable)
        """
        return self._scryfall_data.get("child_ids")

    @property
    def aliases(self) -> list[str] | None:
        """
        Alternate names for this tag.

        Type: Array of Strings (Nullable)
        """
        return self._scryfall_data.get("aliases")

    @property
    def taggings(self) -> list[Any] | None:
        """
        The Tagging objects linking this tag to individual cards.

        Type: Array of Tagging objects
        """
        # Imported lazily to avoid a circular import: tags.py imports this mixin.
        from .tags import Tagging

        return to_object_array(Tagging, "taggings", self._scryfall_data)
