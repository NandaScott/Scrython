"""Usage tests for scrython.migrations.ById."""

import uuid

import scrython.migrations

# The capture script pins whichever migration is listed first, so the specific
# id, strategy, and merged ids drift between refreshes. Assert their shape.
PLACEHOLDER_ID = "12345678-1234-1234-1234-123456789012"


def test_by_id_migration_strategy(stub_response, load_fixture):
    stub_response("migrations/id", load_fixture("migrations_by_id"))
    migration = scrython.migrations.ById(id=PLACEHOLDER_ID)
    assert migration.migration_strategy in {"merge", "delete"}


def test_by_id_migration_old_scryfall_id_is_uuid(stub_response, load_fixture):
    stub_response("migrations/id", load_fixture("migrations_by_id"))
    migration = scrython.migrations.ById(id=PLACEHOLDER_ID)
    assert uuid.UUID(migration.old_scryfall_id)
