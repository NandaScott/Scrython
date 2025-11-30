from typing import Any

from scrython.base import ScrythonRequestHandler
from scrython.base_mixins import ScryfallListMixin

from .migrations_mixins import MigrationsObjectMixin


class Object(MigrationsObjectMixin):
    """
    Wrapper class for individual migration objects from Scryfall API responses.

    Provides access to all migration properties through MigrationsObjectMixin.
    """

    def __init__(self, data: dict[str, Any]) -> None:
        self._scryfall_data = data


class All(ScryfallListMixin, ScrythonRequestHandler):
    """
    Get recent migrations from Scryfall's database.

    Endpoint: GET /migrations

    Returns a paginated list of Migration objects representing recent changes to card
    IDs in Scryfall's database. This endpoint is useful for applications that cache
    card data locally and need to sync with Scryfall's changes.

    Supports pagination via the page parameter.

    Args:
        page: The page number to retrieve (optional, default is 1).

    Example:
        # Get recent migrations
        migrations = scrython.migrations.All()

        # Iterate through migrations
        for migration in migrations.data:
            if migration.migration_strategy == "merge":
                print(f"Card {migration.old_scryfall_id} merged into {migration.new_scryfall_id}")
                if migration.note:
                    print(f"  Note: {migration.note}")
            elif migration.migration_strategy == "delete":
                print(f"Card {migration.old_scryfall_id} was deleted")

        # Check if there are more pages
        if migrations.has_more:
            print("More migrations available via pagination")
            print(f"Next page: {migrations.next_page}")

        # Get a specific page
        page2 = scrython.migrations.All(page=2)

    See: https://scryfall.com/docs/api/migrations
    """

    _endpoint = "/migrations"
    list_data_type = Object


class ById(MigrationsObjectMixin, ScrythonRequestHandler):
    """
    Get a specific migration record by its ID.

    Endpoint: GET /migrations/:id

    Returns a single Migration object identified by its unique Scryfall UUID.

    Args:
        id: The UUID of the migration record (required).

    Example:
        # Get a specific migration by ID
        migration = scrython.migrations.ById(id="12345678-1234-1234-1234-123456789012")

        print(f"Migration performed: {migration.performed_at}")
        print(f"Strategy: {migration.migration_strategy}")
        print(f"Old ID: {migration.old_scryfall_id}")

        if migration.migration_strategy == "merge":
            print(f"New ID: {migration.new_scryfall_id}")
        else:
            print("Card was deleted")

        if migration.note:
            print(f"Note: {migration.note}")

    See: https://scryfall.com/docs/api/migrations
    """

    _endpoint = "/migrations/:id"


class Migrations:
    """
    Smart factory for Migrations API endpoints.

    Routes to the correct migrations endpoint based on provided kwargs.

    Supported parameters:
        - id: Migration UUID → ById
        - (no parameters or page): Get all migrations → All

    Example:
        # Get all recent migrations
        migrations = scrython.Migrations()
        for migration in migrations.data:
            print(f"{migration.old_scryfall_id} → {migration.new_scryfall_id}")

        # Get a specific migration by ID
        migration = scrython.Migrations(id="12345678-1234-1234-1234-123456789012")
        print(f"Strategy: {migration.migration_strategy}")

        # Get a specific page of migrations
        page2 = scrython.Migrations(page=2)
    """

    def __new__(cls, **kwargs):
        if "id" in kwargs:
            return ById(**kwargs)
        else:
            return All(**kwargs)
