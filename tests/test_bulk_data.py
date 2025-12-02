"""Tests for scrython.bulk_data module."""

import gzip
import json
import tempfile
from io import BytesIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from scrython.bulk_data import All, ById, ByType


class TestAll:
    """Test All endpoint."""

    def test_get_all_bulk_data(self, mock_urlopen):
        """Test getting all bulk data."""
        mock_urlopen.set_response("bulk_data/all.json")
        bulk = All()

        assert bulk.scryfall_data.object == "list"
        assert bulk.scryfall_data.has_more is False
        assert len(bulk.scryfall_data.data) == 2

    def test_list_mixin_data_method(self, mock_urlopen):
        """Test that list mixin provides data property."""
        mock_urlopen.set_response("bulk_data/all.json")
        bulk = All()

        bulk_objects = bulk.data
        assert len(bulk_objects) == 2
        assert bulk_objects[0].type == "oracle_cards"
        assert bulk_objects[1].type == "unique_artwork"

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response("bulk_data/all.json")
        _bulk = All()

        assert "api.scryfall.com/bulk-data" in mock_urlopen.calls[0]["url"]


class TestById:
    """Test ById endpoint."""

    def test_get_bulk_data_by_id(self, mock_urlopen):
        """Test getting bulk data by ID."""
        mock_urlopen.set_response("bulk_data/by_id.json")
        bulk = ById(id="27bf3214-1271-490b-bdfe-c0be6c23d02e")

        assert bulk.scryfall_data.object == "bulk_data"
        assert bulk.scryfall_data.id == "27bf3214-1271-490b-bdfe-c0be6c23d02e"
        assert (
            "api.scryfall.com/bulk-data/27bf3214-1271-490b-bdfe-c0be6c23d02e"
            in mock_urlopen.calls[0]["url"]
        )

    def test_missing_id_param(self, mock_urlopen):
        """Test that missing id parameter raises error."""
        mock_urlopen.set_response("bulk_data/by_id.json")

        with pytest.raises(KeyError, match="Missing required path parameter: 'id'"):
            ById()


class TestByType:
    """Test ByType endpoint."""

    def test_get_bulk_data_by_type(self, mock_urlopen):
        """Test getting bulk data by type."""
        mock_urlopen.set_response("bulk_data/by_id.json")
        bulk = ByType(type="oracle_cards")

        assert bulk.scryfall_data.object == "bulk_data"
        assert bulk.scryfall_data.type == "oracle_cards"
        assert "api.scryfall.com/bulk-data/oracle_cards" in mock_urlopen.calls[0]["url"]

    def test_missing_type_param(self, mock_urlopen):
        """Test that missing type parameter raises error."""
        mock_urlopen.set_response("bulk_data/by_id.json")

        with pytest.raises(KeyError, match="Missing required path parameter: 'type'"):
            ByType()


class TestBulkDataMixins:
    """Test bulk data accessor mixins."""

    def test_bulk_data_object_mixin_properties(self, mock_urlopen):
        """Test that bulk data properties are accessible."""
        mock_urlopen.set_response("bulk_data/by_id.json")
        bulk = ById(id="27bf3214-1271-490b-bdfe-c0be6c23d02e")

        assert bulk.type == "oracle_cards"
        assert bulk.name == "Oracle Cards"
        assert (
            bulk.download_uri
            == "https://api.scryfall.com/bulk-data/27bf3214-1271-490b-bdfe-c0be6c23d02e/download"
        )
        assert bulk.updated_at == "2025-01-01T12:00:00.000Z"
        assert bulk.size == 123456789

    def test_bulk_data_object_from_list(self, mock_urlopen):
        """Test that BulkDataObject wrapper works correctly."""
        mock_urlopen.set_response("bulk_data/all.json")
        bulk = All()

        bulk_objects = bulk.data
        assert bulk_objects[0].type == "oracle_cards"
        assert bulk_objects[0].name == "Oracle Cards"
        assert bulk_objects[1].type == "unique_artwork"
        assert bulk_objects[1].name == "Unique Artwork"


class TestBulkDataDownload:
    """Test bulk data download functionality."""

    def test_download_returns_parsed_data(self, mock_urlopen):
        """Test basic download with return_data=True."""
        mock_urlopen.set_response("bulk_data/by_id.json")
        bulk = ByType(type="oracle_cards")

        # Mock the download URL response
        test_data = [{"id": "card1", "name": "Test Card"}]
        compressed_data = gzip.compress(json.dumps(test_data).encode("utf-8"))

        with patch("scrython.bulk_data.bulk_data_mixins.urlopen") as mock_download:
            # Wrap compressed data in BytesIO for proper file-like behavior
            mock_response = BytesIO(compressed_data)
            # Add info() method to mock for header checking
            mock_response.info = MagicMock(
                return_value=MagicMock(get=MagicMock(return_value="gzip"))
            )
            mock_download.return_value.__enter__.return_value = mock_response

            result = bulk.download()

            assert result == test_data
            assert len(result) == 1
            assert result[0]["name"] == "Test Card"

    def test_download_saves_to_file(self, mock_urlopen):
        """Test download with filepath parameter saves file."""
        mock_urlopen.set_response("bulk_data/by_id.json")
        bulk = ByType(type="oracle_cards")

        test_data = [{"id": "card1", "name": "Test Card"}]
        compressed_data = gzip.compress(json.dumps(test_data).encode("utf-8"))

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as tmp:
            tmp_path = tmp.name

        try:
            with patch("scrython.bulk_data.bulk_data_mixins.urlopen") as mock_download:
                # Wrap compressed data in BytesIO for proper file-like behavior
                mock_response = BytesIO(compressed_data)
                # Add info() method to mock for header checking
                mock_response.info = MagicMock(
                    return_value=MagicMock(get=MagicMock(return_value="gzip"))
                )
                mock_download.return_value.__enter__.return_value = mock_response

                result = bulk.download(filepath=tmp_path)

                # Should still return data
                assert result == test_data

                # File should exist and contain correct data
                assert Path(tmp_path).exists()
                with open(tmp_path, encoding="utf-8") as f:
                    saved_data = json.load(f)
                assert saved_data == test_data
        finally:
            # Cleanup
            Path(tmp_path).unlink(missing_ok=True)

    def test_download_without_return_data(self, mock_urlopen):
        """Test download with return_data=False."""
        mock_urlopen.set_response("bulk_data/by_id.json")
        bulk = ByType(type="oracle_cards")

        test_data = [{"id": "card1", "name": "Test Card"}]
        compressed_data = gzip.compress(json.dumps(test_data).encode("utf-8"))

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as tmp:
            tmp_path = tmp.name

        try:
            with patch("scrython.bulk_data.bulk_data_mixins.urlopen") as mock_download:
                # Wrap compressed data in BytesIO for proper file-like behavior
                mock_response = BytesIO(compressed_data)
                # Add info() method to mock for header checking
                mock_response.info = MagicMock(
                    return_value=MagicMock(get=MagicMock(return_value="gzip"))
                )
                mock_download.return_value.__enter__.return_value = mock_response

                result = bulk.download(filepath=tmp_path, return_data=False)

                # Should return None
                assert result is None

                # File should still be saved
                assert Path(tmp_path).exists()
                with open(tmp_path, encoding="utf-8") as f:
                    saved_data = json.load(f)
                assert saved_data == test_data
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_download_with_invalid_gzip(self, mock_urlopen):
        """Test that invalid gzip data raises error."""
        mock_urlopen.set_response("bulk_data/by_id.json")
        bulk = ByType(type="oracle_cards")

        with patch("scrython.bulk_data.bulk_data_mixins.urlopen") as mock_download:
            mock_response = MagicMock()
            mock_response.read.return_value = b"not gzipped data"
            mock_response.info.return_value.get.return_value = "gzip"  # Claims to be gzip but isn't
            mock_response.__enter__.return_value = mock_response
            mock_response.__exit__.return_value = None
            mock_download.return_value = mock_response

            with pytest.raises((gzip.BadGzipFile, Exception)):
                bulk.download()

    def test_download_with_invalid_json(self, mock_urlopen):
        """Test that invalid JSON raises error."""
        mock_urlopen.set_response("bulk_data/by_id.json")
        bulk = ByType(type="oracle_cards")

        invalid_json = b"not valid json"
        compressed_data = gzip.compress(invalid_json)

        with patch("scrython.bulk_data.bulk_data_mixins.urlopen") as mock_download:
            # Wrap compressed data in BytesIO for proper file-like behavior
            mock_response = BytesIO(compressed_data)
            # Add info() method to mock for header checking
            mock_response.info = MagicMock(
                return_value=MagicMock(get=MagicMock(return_value="gzip"))
            )
            mock_download.return_value.__enter__.return_value = mock_response

            with pytest.raises(json.JSONDecodeError):
                bulk.download()

    def test_download_progress_without_tqdm_raises_import_error(self, mock_urlopen):
        """Test that progress=True without tqdm raises ImportError."""
        mock_urlopen.set_response("bulk_data/by_id.json")
        bulk = ByType(type="oracle_cards")

        with (
            patch("scrython.bulk_data.bulk_data_mixins.urlopen"),
            patch.dict("sys.modules", {"tqdm": None}),
            pytest.raises(ImportError, match="tqdm is required"),
        ):
            bulk.download(progress=True)

    def test_download_uncompressed_no_progress(self, mock_urlopen):
        """Test download handles uncompressed JSON without progress bar."""
        mock_urlopen.set_response("bulk_data/by_id.json")
        bulk = ByType(type="oracle_cards")

        # Test with plain JSON (not gzip compressed)
        test_data = [{"id": "card1", "name": "Test Card"}]
        plain_json = json.dumps(test_data).encode("utf-8")

        with patch("scrython.bulk_data.bulk_data_mixins.urlopen") as mock_download:
            # Create mock with NO Content-Encoding header (empty string)
            mock_response = MagicMock()
            mock_response.read.return_value = plain_json
            mock_response.info.return_value.get.return_value = ""  # No encoding header
            mock_response.__enter__.return_value = mock_response
            mock_response.__exit__.return_value = None
            mock_download.return_value = mock_response

            result = bulk.download()

            assert result == test_data
            assert len(result) == 1
            assert result[0]["name"] == "Test Card"

    def test_download_uncompressed_with_progress(self, mock_urlopen):
        """Test download handles uncompressed JSON with progress bar."""
        # Skip if tqdm is not installed
        pytest.importorskip("tqdm")

        mock_urlopen.set_response("bulk_data/by_id.json")
        bulk = ByType(type="oracle_cards")

        # Test with plain JSON (not gzip compressed)
        test_data = [{"id": "card1", "name": "Test Card"}]
        plain_json = json.dumps(test_data).encode("utf-8")

        with patch("scrython.bulk_data.bulk_data_mixins.urlopen") as mock_download:
            # Create mock with NO Content-Encoding header
            mock_response = MagicMock()
            mock_response.read.side_effect = [
                plain_json,
                b"",
            ]  # Return data then empty to signal EOF
            mock_response.headers.get.return_value = str(len(plain_json))
            mock_response.info.return_value.get.return_value = ""  # No encoding header
            mock_response.__enter__.return_value = mock_response
            mock_response.__exit__.return_value = None
            mock_download.return_value = mock_response

            result = bulk.download(progress=True)

            assert result == test_data
            assert len(result) == 1
            assert result[0]["name"] == "Test Card"
