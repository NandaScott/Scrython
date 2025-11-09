"""Tests for scrython.bulk_data module."""
import pytest
from scrython.bulk_data.bulk_data import AllBulkData, BulkDataById, BulkDataByType, BulkData


class TestAllBulkData:
    """Test AllBulkData endpoint."""

    def test_get_all_bulk_data(self, mock_urlopen):
        """Test getting all bulk data."""
        mock_urlopen.set_response('bulk_data/all.json')
        bulk = AllBulkData()

        assert bulk.scryfall_data['object'] == 'list'
        assert bulk.scryfall_data['has_more'] is False
        assert len(bulk.scryfall_data['data']) == 2

    def test_list_mixin_data_method(self, mock_urlopen):
        """Test that list mixin provides data property."""
        mock_urlopen.set_response('bulk_data/all.json')
        bulk = AllBulkData()

        bulk_objects = bulk.data
        assert len(bulk_objects) == 2
        assert bulk_objects[0].type == 'oracle_cards'
        assert bulk_objects[1].type == 'unique_artwork'

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response('bulk_data/all.json')
        bulk = AllBulkData()

        assert 'api.scryfall.com/bulk-data' in mock_urlopen.calls[0]['url']


class TestBulkDataById:
    """Test BulkDataById endpoint."""

    def test_get_bulk_data_by_id(self, mock_urlopen):
        """Test getting bulk data by ID."""
        mock_urlopen.set_response('bulk_data/by_id.json')
        bulk = BulkDataById(id='27bf3214-1271-490b-bdfe-c0be6c23d02e')

        assert bulk.scryfall_data['object'] == 'bulk_data'
        assert bulk.scryfall_data['id'] == '27bf3214-1271-490b-bdfe-c0be6c23d02e'
        assert 'api.scryfall.com/bulk-data/27bf3214-1271-490b-bdfe-c0be6c23d02e' in mock_urlopen.calls[0]['url']

    def test_missing_id_param(self, mock_urlopen):
        """Test that missing id parameter raises error."""
        mock_urlopen.set_response('bulk_data/by_id.json')

        with pytest.raises(KeyError, match="Missing required path parameter: 'id'"):
            BulkDataById()


class TestBulkDataByType:
    """Test BulkDataByType endpoint."""

    def test_get_bulk_data_by_type(self, mock_urlopen):
        """Test getting bulk data by type."""
        mock_urlopen.set_response('bulk_data/by_id.json')
        bulk = BulkDataByType(type='oracle_cards')

        assert bulk.scryfall_data['object'] == 'bulk_data'
        assert bulk.scryfall_data['type'] == 'oracle_cards'
        assert 'api.scryfall.com/bulk-data/oracle_cards' in mock_urlopen.calls[0]['url']

    def test_missing_type_param(self, mock_urlopen):
        """Test that missing type parameter raises error."""
        mock_urlopen.set_response('bulk_data/by_id.json')

        with pytest.raises(KeyError, match="Missing required path parameter: 'type'"):
            BulkDataByType()


class TestBulkDataFactory:
    """Test the BulkData factory class routing logic."""

    def test_factory_routes_by_id(self, mock_urlopen):
        """Test that BulkData factory routes to BulkDataById."""
        mock_urlopen.set_response('bulk_data/by_id.json')
        result = BulkData(id='27bf3214-1271-490b-bdfe-c0be6c23d02e')

        assert isinstance(result, BulkDataById)
        assert 'api.scryfall.com/bulk-data/27bf3214-1271-490b-bdfe-c0be6c23d02e' in mock_urlopen.calls[0]['url']

    def test_factory_routes_by_type(self, mock_urlopen):
        """Test that BulkData factory routes to BulkDataByType."""
        mock_urlopen.set_response('bulk_data/by_id.json')
        result = BulkData(type='oracle_cards')

        assert isinstance(result, BulkDataByType)
        assert 'api.scryfall.com/bulk-data/oracle_cards' in mock_urlopen.calls[0]['url']

    def test_factory_defaults_to_all_bulk_data(self, mock_urlopen):
        """Test that BulkData factory defaults to AllBulkData when no parameters provided."""
        mock_urlopen.set_response('bulk_data/all.json')
        result = BulkData()

        assert isinstance(result, AllBulkData)
        assert 'api.scryfall.com/bulk-data' in mock_urlopen.calls[0]['url']


class TestBulkDataMixins:
    """Test bulk data accessor mixins."""

    def test_bulk_data_object_mixin_properties(self, mock_urlopen):
        """Test that bulk data properties are accessible."""
        mock_urlopen.set_response('bulk_data/by_id.json')
        bulk = BulkData(id='27bf3214-1271-490b-bdfe-c0be6c23d02e')

        assert bulk.type == 'oracle_cards'
        assert bulk.name == 'Oracle Cards'
        assert bulk.download_uri == 'https://api.scryfall.com/bulk-data/27bf3214-1271-490b-bdfe-c0be6c23d02e/download'
        assert bulk.updated_at == '2025-01-01T12:00:00.000Z'
        assert bulk.size == 123456789

    def test_bulk_data_object_from_list(self, mock_urlopen):
        """Test that BulkDataObject wrapper works correctly."""
        mock_urlopen.set_response('bulk_data/all.json')
        bulk = BulkData()

        bulk_objects = bulk.data
        assert bulk_objects[0].type == 'oracle_cards'
        assert bulk_objects[0].name == 'Oracle Cards'
        assert bulk_objects[1].type == 'unique_artwork'
        assert bulk_objects[1].name == 'Unique Artwork'
