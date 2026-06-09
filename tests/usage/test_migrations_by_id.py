"""Usage tests for scrython.migrations.ById."""

import scrython.migrations

# A pinned, immutable historical migration (merge strategy).
MIGRATION_ID = "f75b2d8b-c73b-4352-91f7-3b9239bd3c9f"


def test_by_id__id__migration_strategy(migrations_by_id__merge):
    migration = scrython.migrations.ById(id=MIGRATION_ID)
    assert migration.migration_strategy == "merge"


def test_by_id__id__migration_old_scryfall_id(migrations_by_id__merge):
    migration = scrython.migrations.ById(id=MIGRATION_ID)
    assert migration.old_scryfall_id == "c765c1a3-5bc3-46ff-9818-842815c52984"
