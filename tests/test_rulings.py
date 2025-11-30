"""Tests for scrython.rulings module."""

import pytest

from scrython.rulings import (
    ByArenaId,
    ByCodeNumber,
    ById,
    ByMTGOId,
    ByMultiverseId,
    Rulings,
)


class TestById:
    """Test ById endpoint."""

    def test_get_rulings_by_id(self, mock_urlopen):
        """Test getting rulings by Scryfall ID."""
        mock_urlopen.set_response("rulings/by_id.json")
        rulings = ById(id="f2b9983e-20d4-4d12-9e2c-ec6d9a345787")

        assert rulings.object == "list"
        assert rulings.has_more is False
        assert len(rulings.data) == 3

    def test_list_mixin_data_method(self, mock_urlopen):
        """Test that list mixin provides data property."""
        mock_urlopen.set_response("rulings/by_id.json")
        rulings = ById(id="f2b9983e-20d4-4d12-9e2c-ec6d9a345787")

        ruling_objects = rulings.data
        assert len(ruling_objects) == 3
        assert ruling_objects[0].source == "wotc"
        assert ruling_objects[1].source == "wotc"
        assert ruling_objects[2].source == "scryfall"

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response("rulings/by_id.json")
        _rulings = ById(id="f2b9983e-20d4-4d12-9e2c-ec6d9a345787")

        assert (
            "api.scryfall.com/cards/f2b9983e-20d4-4d12-9e2c-ec6d9a345787/rulings"
            in mock_urlopen.calls[0]["url"]
        )

    def test_missing_id_param(self, mock_urlopen):
        """Test that missing id parameter raises error."""
        mock_urlopen.set_response("rulings/by_id.json")

        with pytest.raises(KeyError, match="Missing required path parameter: 'id'"):
            ById()


class TestByMultiverseId:
    """Test ByMultiverseId endpoint."""

    def test_get_rulings_by_multiverse_id(self, mock_urlopen):
        """Test getting rulings by Multiverse ID."""
        mock_urlopen.set_response("rulings/by_id.json")
        rulings = ByMultiverseId(id=3749)

        assert rulings.object == "list"
        assert "api.scryfall.com/cards/multiverse/3749/rulings" in mock_urlopen.calls[0]["url"]

    def test_missing_id_param(self, mock_urlopen):
        """Test that missing id parameter raises error."""
        mock_urlopen.set_response("rulings/by_id.json")

        with pytest.raises(KeyError, match="Missing required path parameter: 'id'"):
            ByMultiverseId()


class TestByMTGOId:
    """Test ByMTGOId endpoint."""

    def test_get_rulings_by_mtgo_id(self, mock_urlopen):
        """Test getting rulings by MTGO ID."""
        mock_urlopen.set_response("rulings/by_id.json")
        rulings = ByMTGOId(id=54321)

        assert rulings.object == "list"
        assert "api.scryfall.com/cards/mtgo/54321/rulings" in mock_urlopen.calls[0]["url"]

    def test_missing_id_param(self, mock_urlopen):
        """Test that missing id parameter raises error."""
        mock_urlopen.set_response("rulings/by_id.json")

        with pytest.raises(KeyError, match="Missing required path parameter: 'id'"):
            ByMTGOId()


class TestByArenaId:
    """Test ByArenaId endpoint."""

    def test_get_rulings_by_arena_id(self, mock_urlopen):
        """Test getting rulings by Arena ID."""
        mock_urlopen.set_response("rulings/by_id.json")
        rulings = ByArenaId(id=67890)

        assert rulings.object == "list"
        assert "api.scryfall.com/cards/arena/67890/rulings" in mock_urlopen.calls[0]["url"]

    def test_missing_id_param(self, mock_urlopen):
        """Test that missing id parameter raises error."""
        mock_urlopen.set_response("rulings/by_id.json")

        with pytest.raises(KeyError, match="Missing required path parameter: 'id'"):
            ByArenaId()


class TestByCodeNumber:
    """Test ByCodeNumber endpoint."""

    def test_get_rulings_by_code_number(self, mock_urlopen):
        """Test getting rulings by set code and collector number."""
        mock_urlopen.set_response("rulings/by_code_number.json")
        rulings = ByCodeNumber(code="znr", number="232")

        assert rulings.object == "list"
        assert rulings.has_more is False
        assert len(rulings.data) == 2
        assert "api.scryfall.com/cards/znr/232/rulings" in mock_urlopen.calls[0]["url"]

    def test_missing_code_param(self, mock_urlopen):
        """Test that missing code parameter raises error."""
        mock_urlopen.set_response("rulings/by_code_number.json")

        with pytest.raises(KeyError, match="Missing required path parameter: 'code'"):
            ByCodeNumber(number="232")

    def test_missing_number_param(self, mock_urlopen):
        """Test that missing number parameter raises error."""
        mock_urlopen.set_response("rulings/by_code_number.json")

        with pytest.raises(KeyError, match="Missing required path parameter: 'number'"):
            ByCodeNumber(code="znr")


class TestRulingsMixins:
    """Test rulings data accessor mixins."""

    def test_rulings_object_mixin_properties(self, mock_urlopen):
        """Test that ruling properties are accessible."""
        mock_urlopen.set_response("rulings/by_id.json")
        rulings = ById(id="f2b9983e-20d4-4d12-9e2c-ec6d9a345787")

        ruling_objects = rulings.data
        first_ruling = ruling_objects[0]

        assert first_ruling.object == "ruling"
        assert first_ruling.oracle_id == "f2b9983e-20d4-4d12-9e2c-ec6d9a345787"
        assert first_ruling.source == "wotc"
        assert first_ruling.published_at == "2020-08-07"
        assert "convoke" in first_ruling.comment.lower()

    def test_rulings_object_from_list(self, mock_urlopen):
        """Test that RulingsObject wrapper works correctly."""
        mock_urlopen.set_response("rulings/by_id.json")
        rulings = ById(id="f2b9983e-20d4-4d12-9e2c-ec6d9a345787")

        ruling_objects = rulings.data
        assert ruling_objects[0].source == "wotc"
        assert ruling_objects[1].source == "wotc"
        assert ruling_objects[2].source == "scryfall"

    def test_filter_by_source(self, mock_urlopen):
        """Test filtering rulings by source."""
        mock_urlopen.set_response("rulings/by_id.json")
        rulings = ById(id="f2b9983e-20d4-4d12-9e2c-ec6d9a345787")

        wotc_rulings = [r for r in rulings.data if r.source == "wotc"]
        scryfall_rulings = [r for r in rulings.data if r.source == "scryfall"]

        assert len(wotc_rulings) == 2
        assert len(scryfall_rulings) == 1


class TestRulingsFactory:
    """Test Rulings smart factory."""

    def test_factory_routes_to_by_id(self, mock_urlopen):
        """Test that factory routes to ById when given id parameter."""
        mock_urlopen.set_response("rulings/by_id.json")
        rulings = Rulings(id="f2b9983e-20d4-4d12-9e2c-ec6d9a345787")

        assert isinstance(rulings, ById)
        assert (
            "api.scryfall.com/cards/f2b9983e-20d4-4d12-9e2c-ec6d9a345787/rulings"
            in mock_urlopen.calls[0]["url"]
        )

    def test_factory_routes_to_by_multiverse_id(self, mock_urlopen):
        """Test that factory routes to ByMultiverseId when given multiverse_id parameter."""
        mock_urlopen.set_response("rulings/by_id.json")
        rulings = Rulings(multiverse_id=3749)

        assert isinstance(rulings, ByMultiverseId)
        assert "api.scryfall.com/cards/multiverse/3749/rulings" in mock_urlopen.calls[0]["url"]

    def test_factory_routes_to_by_mtgo_id(self, mock_urlopen):
        """Test that factory routes to ByMTGOId when given mtgo_id parameter."""
        mock_urlopen.set_response("rulings/by_id.json")
        rulings = Rulings(mtgo_id=54321)

        assert isinstance(rulings, ByMTGOId)
        assert "api.scryfall.com/cards/mtgo/54321/rulings" in mock_urlopen.calls[0]["url"]

    def test_factory_routes_to_by_arena_id(self, mock_urlopen):
        """Test that factory routes to ByArenaId when given arena_id parameter."""
        mock_urlopen.set_response("rulings/by_id.json")
        rulings = Rulings(arena_id=67890)

        assert isinstance(rulings, ByArenaId)
        assert "api.scryfall.com/cards/arena/67890/rulings" in mock_urlopen.calls[0]["url"]

    def test_factory_routes_to_by_code_number(self, mock_urlopen):
        """Test that factory routes to ByCodeNumber when given code and number parameters."""
        mock_urlopen.set_response("rulings/by_code_number.json")
        rulings = Rulings(code="znr", number="232")

        assert isinstance(rulings, ByCodeNumber)
        assert "api.scryfall.com/cards/znr/232/rulings" in mock_urlopen.calls[0]["url"]

    def test_factory_raises_error_for_invalid_params(self, mock_urlopen):
        """Test that factory raises error for invalid parameters."""
        mock_urlopen.set_response("rulings/by_id.json")

        with pytest.raises(ValueError, match="Invalid parameters for Rulings"):
            Rulings()

        with pytest.raises(ValueError, match="Invalid parameters for Rulings"):
            Rulings(invalid_param="test")
