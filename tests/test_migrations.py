"""Tests for scrython.migrations module."""

import pytest

from scrython.migrations import All, ById, Migrations


class TestAll:
    """Test All endpoint."""

    def test_get_all_migrations(self, mock_urlopen):
        """Test getting all migrations."""
        mock_urlopen.set_response("migrations/all.json")
        migrations = All()

        assert migrations.object == "list"
        assert migrations.has_more is True
        assert len(migrations.data) == 2

    def test_list_mixin_data_method(self, mock_urlopen):
        """Test that list mixin provides data property."""
        mock_urlopen.set_response("migrations/all.json")
        migrations = All()

        migration_objects = migrations.data
        assert len(migration_objects) == 2
        assert migration_objects[0].migration_strategy == "merge"
        assert migration_objects[1].migration_strategy == "delete"

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response("migrations/all.json")
        _migrations = All()

        assert "api.scryfall.com/migrations" in mock_urlopen.calls[0]["url"]

    def test_pagination(self, mock_urlopen):
        """Test pagination with page parameter."""
        mock_urlopen.set_response("migrations/all.json")
        _migrations = All(page=2)

        assert "api.scryfall.com/migrations" in mock_urlopen.calls[0]["url"]
        assert "page=2" in mock_urlopen.calls[0]["url"]


class TestById:
    """Test ById endpoint."""

    def test_get_migration_by_id(self, mock_urlopen):
        """Test getting a migration by ID."""
        mock_urlopen.set_response("migrations/by_id.json")
        migration = ById(id="12345678-1234-1234-1234-123456789012")

        assert migration.object == "migration"
        assert migration.id == "12345678-1234-1234-1234-123456789012"
        assert migration.migration_strategy == "merge"

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response("migrations/by_id.json")
        _migration = ById(id="12345678-1234-1234-1234-123456789012")

        assert (
            "api.scryfall.com/migrations/12345678-1234-1234-1234-123456789012"
            in mock_urlopen.calls[0]["url"]
        )

    def test_missing_id_param(self, mock_urlopen):
        """Test that missing id parameter raises error."""
        mock_urlopen.set_response("migrations/by_id.json")

        with pytest.raises(KeyError, match="Missing required path parameter: 'id'"):
            ById()


class TestMigrationsMixins:
    """Test migrations data accessor mixins."""

    def test_migrations_object_mixin_properties(self, mock_urlopen):
        """Test that migration properties are accessible."""
        mock_urlopen.set_response("migrations/by_id.json")
        migration = ById(id="12345678-1234-1234-1234-123456789012")

        assert migration.object == "migration"
        assert migration.id == "12345678-1234-1234-1234-123456789012"
        assert (
            migration.uri
            == "https://api.scryfall.com/migrations/12345678-1234-1234-1234-123456789012"
        )
        assert migration.performed_at == "2024-01-15T10:30:00.000Z"
        assert migration.migration_strategy == "merge"
        assert migration.old_scryfall_id == "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
        assert migration.new_scryfall_id == "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
        assert migration.note == "Duplicate card merged into canonical version"
        assert migration.metadata is not None
        assert migration.metadata["reason"] == "duplicate"

    def test_merge_migration_properties(self, mock_urlopen):
        """Test properties of a merge migration."""
        mock_urlopen.set_response("migrations/all.json")
        migrations = All()

        merge_migration = migrations.data[0]
        assert merge_migration.migration_strategy == "merge"
        assert merge_migration.old_scryfall_id == "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
        assert merge_migration.new_scryfall_id == "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
        assert merge_migration.note is not None

    def test_delete_migration_properties(self, mock_urlopen):
        """Test properties of a delete migration."""
        mock_urlopen.set_response("migrations/all.json")
        migrations = All()

        delete_migration = migrations.data[1]
        assert delete_migration.migration_strategy == "delete"
        assert delete_migration.old_scryfall_id == "cccccccc-cccc-cccc-cccc-cccccccccccc"
        assert delete_migration.new_scryfall_id is None
        assert delete_migration.note is not None

    def test_filter_by_strategy(self, mock_urlopen):
        """Test filtering migrations by strategy."""
        mock_urlopen.set_response("migrations/all.json")
        migrations = All()

        merge_migrations = [m for m in migrations.data if m.migration_strategy == "merge"]
        delete_migrations = [m for m in migrations.data if m.migration_strategy == "delete"]

        assert len(merge_migrations) == 1
        assert len(delete_migrations) == 1


class TestMigrationsFactory:
    """Test Migrations smart factory."""

    def test_factory_routes_to_all(self, mock_urlopen):
        """Test that factory routes to All when no parameters given."""
        mock_urlopen.set_response("migrations/all.json")
        migrations = Migrations()

        assert isinstance(migrations, All)
        assert "api.scryfall.com/migrations" in mock_urlopen.calls[0]["url"]

    def test_factory_routes_to_all_with_page(self, mock_urlopen):
        """Test that factory routes to All when given page parameter."""
        mock_urlopen.set_response("migrations/all.json")
        migrations = Migrations(page=2)

        assert isinstance(migrations, All)
        assert "api.scryfall.com/migrations" in mock_urlopen.calls[0]["url"]
        assert "page=2" in mock_urlopen.calls[0]["url"]

    def test_factory_routes_to_by_id(self, mock_urlopen):
        """Test that factory routes to ById when given id parameter."""
        mock_urlopen.set_response("migrations/by_id.json")
        migration = Migrations(id="12345678-1234-1234-1234-123456789012")

        assert isinstance(migration, ById)
        assert (
            "api.scryfall.com/migrations/12345678-1234-1234-1234-123456789012"
            in mock_urlopen.calls[0]["url"]
        )
