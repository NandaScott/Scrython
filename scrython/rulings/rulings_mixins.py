from typing import Any


class RulingsObjectMixin:
    """Provides property accessors for ruling objects from the Scryfall API."""

    _scryfall_data: dict[str, Any]

    @property
    def object(self) -> str:
        """
        A content type for this object, always ruling.

        Type: String (Required)
        """
        return "ruling"

    @property
    def oracle_id(self) -> str:
        """
        The Oracle ID for the card this ruling is about.

        Type: UUID (Required)
        """
        return self._scryfall_data["oracle_id"]

    @property
    def source(self) -> str:
        """
        The source of this ruling. Either "wotc" (Wizards of the Coast) or "scryfall".

        Type: String (Required)
        """
        return self._scryfall_data["source"]

    @property
    def published_at(self) -> str:
        """
        The date this ruling was published, in ISO 8601 format (YYYY-MM-DD).

        Type: Date (Required)
        """
        return self._scryfall_data["published_at"]

    @property
    def comment(self) -> str:
        """
        The text of the ruling.

        Type: String (Required)
        """
        return self._scryfall_data["comment"]
