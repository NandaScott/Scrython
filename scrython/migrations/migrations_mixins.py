from typing import Any


class MigrationsObjectMixin:
    """Provides property accessors for migration objects from the Scryfall API."""

    _scryfall_data: dict[str, Any]

    @property
    def object(self) -> str:
        """
        A content type for this object, always migration.

        Type: String (Required)
        """
        return "migration"

    @property
    def id(self) -> str:
        """
        The unique ID for this migration record.

        Type: UUID (Required)
        """
        return self._scryfall_data["id"]

    @property
    def uri(self) -> str:
        """
        A link to this migration record on Scryfall's API.

        Type: URI (Required)
        """
        return self._scryfall_data["uri"]

    @property
    def performed_at(self) -> str:
        """
        The date and time when this migration was performed (ISO 8601 format).

        Type: Timestamp (Required)
        """
        return self._scryfall_data["performed_at"]

    @property
    def migration_strategy(self) -> str:
        """
        The migration strategy that was used. Either "merge" or "delete".

        Type: String (Required)

        - "merge": The old card was merged into a new card
        - "delete": The old card was deleted without replacement
        """
        return self._scryfall_data["migration_strategy"]

    @property
    def old_scryfall_id(self) -> str:
        """
        The original Scryfall ID that was migrated.

        Type: UUID (Required)
        """
        return self._scryfall_data["old_scryfall_id"]

    @property
    def new_scryfall_id(self) -> str | None:
        """
        The new Scryfall ID that replaced the old one, if the strategy was "merge".

        Type: UUID (Nullable)

        Note: Will be None if the migration_strategy is "delete".
        """
        return self._scryfall_data.get("new_scryfall_id")

    @property
    def note(self) -> str | None:
        """
        An optional explanation from the Scryfall team about this migration.

        Type: String (Nullable)
        """
        return self._scryfall_data.get("note")

    @property
    def metadata(self) -> dict[str, Any] | None:
        """
        Additional context data about this migration.

        Type: Object (Nullable)
        """
        return self._scryfall_data.get("metadata")
