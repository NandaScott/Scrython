"""Usage tests for scrython.migrations.ById."""

import scrython.migrations


def test_by_id_migration_strategy(stub_response, load_fixture):
    stub_response("migrations/id", load_fixture("migrations_by_id"))
    migration = scrython.migrations.ById(id="12345678-1234-1234-1234-123456789012")
    assert migration.migration_strategy == "merge"


def test_by_id_migration_old_scryfall_id(stub_response, load_fixture):
    stub_response("migrations/id", load_fixture("migrations_by_id"))
    migration = scrython.migrations.ById(id="12345678-1234-1234-1234-123456789012")
    assert migration.old_scryfall_id == "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
