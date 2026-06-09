from typing import Any

from ..types import ScryfallTagData, ScryfallTaggingData
from ..utils import to_object_array


class TaggingObjectMixin:
    """Provides property accessors for tagging objects nested in a Tag."""

    _scryfall_data: ScryfallTaggingData

    @property
    def illustration_id(self) -> str | None:
        """
        For art tags: the illustration_id of the card artwork that has this tagging.

        Type: UUID (Nullable)
        """
        return self._scryfall_data.get("illustration_id")

    @property
    def oracle_id(self) -> str | None:
        """
        For oracle tags: the oracle_id of the card that has this tagging.

        Type: UUID (Nullable)
        """
        return self._scryfall_data.get("oracle_id")

    @property
    def weight(self) -> str:
        """
        How prominently the tag applies to this card. One of "very_strong" (the
        subject is exemplary for the image or card text), "strong" (a primary
        focus), "median" (a normal tagging with no special weight), or "weak"
        (a minor detail or background element).

        Type: String (Required)
        """
        return self._scryfall_data["weight"]

    @property
    def annotation(self) -> str | None:
        """
        An optional note providing additional context for this specific tagging.

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
        A unique and stable UUID for this tag.

        Type: UUID (Required)
        """
        return self._scryfall_data["id"]

    @property
    def slug(self) -> str:
        """
        A URL-safe identifier for the tag, e.g. "squirrel". Slugs may change over
        time; use id as a stable reference.

        Type: String (Required)
        """
        return self._scryfall_data["slug"]

    @property
    def label(self) -> str:
        """
        A human-readable name for this tag, e.g. "Squirrel".

        Type: String (Required)
        """
        return self._scryfall_data["label"]

    @property
    def uri(self) -> str:
        """
        A link to this tag on the Tagger site.

        Type: URI (Required)
        """
        return self._scryfall_data["uri"]

    @property
    def type(self) -> str:
        """
        The tag type: "illustration" for art tags or "oracle" for oracle tags.

        Type: String (Required)
        """
        return self._scryfall_data["type"]

    @property
    def description(self) -> str | None:
        """
        An optional description of what this tag represents.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("description")

    @property
    def parent_ids(self) -> list[str] | None:
        """
        UUIDs of parent tags in the tag hierarchy within this bulk file.

        Type: Array (Nullable)
        """
        return self._scryfall_data.get("parent_ids")

    @property
    def child_ids(self) -> list[str] | None:
        """
        UUIDs of child tags in the tag hierarchy within this bulk file.

        Type: Array (Nullable)
        """
        return self._scryfall_data.get("child_ids")

    @property
    def aliases(self) -> list[str] | None:
        """
        Alternative names the community uses for this tag.

        Type: Array (Nullable)
        """
        return self._scryfall_data.get("aliases")

    @property
    def taggings(self) -> list[Any]:
        """
        An array of tagging objects associating this tag with specific cards.

        Type: Array (Required)
        """
        # Imported lazily to avoid a circular import: tags.py imports this mixin.
        from .tags import Tagging

        # taggings is a required field; return an empty list rather than None when
        # the key is absent so callers can always iterate without a None check.
        taggings = to_object_array(Tagging, "taggings", self._scryfall_data)
        return taggings if taggings is not None else []
