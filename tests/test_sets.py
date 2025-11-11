"""Tests for scrython.sets module."""

import pytest

from scrython.sets import All, ByCode, ById, ByTCGPlayerId


class TestAll:
    """Test All endpoint."""

    def test_get_all_sets(self, mock_urlopen):
        """Test getting all sets."""
        mock_urlopen.set_response("sets/all.json")
        sets = All()

        assert sets.scryfall_data.object == "list"
        assert sets.scryfall_data.has_more is False
        assert len(sets.scryfall_data.data) == 2

    def test_list_mixin_data_method(self, mock_urlopen):
        """Test that list mixin provides data property."""
        mock_urlopen.set_response("sets/all.json")
        sets = All()

        set_objects = sets.data
        assert len(set_objects) == 2
        assert set_objects[0].code == "lea"
        assert set_objects[1].code == "leb"

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response("sets/all.json")
        _sets = All()

        assert "api.scryfall.com/sets" in mock_urlopen.calls[0]["url"]


class TestByCode:
    """Test ByCode endpoint."""

    def test_get_set_by_code(self, mock_urlopen):
        """Test getting a set by code."""
        mock_urlopen.set_response("sets/by_code.json")
        set_obj = ByCode(code="lea")

        assert set_obj.scryfall_data.object == "set"
        assert set_obj.scryfall_data.code == "lea"
        assert "api.scryfall.com/sets/lea" in mock_urlopen.calls[0]["url"]

    def test_missing_code_param(self, mock_urlopen):
        """Test that missing code parameter raises error."""
        mock_urlopen.set_response("sets/by_code.json")

        with pytest.raises(KeyError, match="Missing required path parameter: 'code'"):
            ByCode()


class TestByTCGPlayerId:
    """Test ByTCGPlayerId endpoint."""

    def test_get_set_by_tcgplayer_id(self, mock_urlopen):
        """Test getting a set by TCGPlayer ID."""
        mock_urlopen.set_response("sets/by_code.json")
        set_obj = ByTCGPlayerId(id="12345")

        assert set_obj.scryfall_data.object == "set"
        assert "api.scryfall.com/sets/tcgplayer/12345" in mock_urlopen.calls[0]["url"]

    def test_missing_id_param(self, mock_urlopen):
        """Test that missing id parameter raises error."""
        mock_urlopen.set_response("sets/by_code.json")

        with pytest.raises(KeyError, match="Missing required path parameter: 'id'"):
            ByTCGPlayerId()


class TestById:
    """Test ById endpoint."""

    def test_get_set_by_id(self, mock_urlopen):
        """Test getting a set by Scryfall ID."""
        mock_urlopen.set_response("sets/by_code.json")
        set_obj = ById(id="288bd996-960e-488e-a4e7-b6571934c371")

        assert set_obj.scryfall_data.object == "set"
        assert (
            "api.scryfall.com/sets/288bd996-960e-488e-a4e7-b6571934c371"
            in mock_urlopen.calls[0]["url"]
        )

    def test_missing_id_param(self, mock_urlopen):
        """Test that missing id parameter raises error."""
        mock_urlopen.set_response("sets/by_code.json")

        with pytest.raises(KeyError, match="Missing required path parameter: 'id'"):
            ById()


class TestSetsMixins:
    """Test sets data accessor mixins."""

    def test_sets_object_mixin_properties(self, mock_urlopen):
        """Test that set properties are accessible."""
        mock_urlopen.set_response("sets/by_code.json")
        set_obj = ByCode(code="lea")

        assert set_obj.code == "lea"
        assert set_obj.name == "Limited Edition Alpha"
        assert set_obj.set_type == "core"
        assert set_obj.card_count == 295
        assert set_obj.released_at == "1993-08-05"

    def test_sets_object_from_list(self, mock_urlopen):
        """Test that SetsObject wrapper works correctly."""
        mock_urlopen.set_response("sets/all.json")
        sets = All()

        set_objects = sets.data
        assert set_objects[0].code == "lea"
        assert set_objects[0].name == "Limited Edition Alpha"
        assert set_objects[1].code == "leb"
        assert set_objects[1].name == "Limited Edition Beta"
