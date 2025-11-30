"""Tests for scrython.symbology module."""

from scrython.symbology import All, ParseMana, Symbology


class TestAll:
    """Test All endpoint."""

    def test_get_all_symbols(self, mock_urlopen):
        """Test getting all card symbols."""
        mock_urlopen.set_response("symbology/all.json")
        symbols = All()

        assert symbols.object == "list"
        assert symbols.has_more is False
        assert len(symbols.data) == 4

    def test_list_mixin_data_method(self, mock_urlopen):
        """Test that list mixin provides data property."""
        mock_urlopen.set_response("symbology/all.json")
        symbols = All()

        symbol_objects = symbols.data
        assert len(symbol_objects) == 4
        assert symbol_objects[0].symbol == "{W}"
        assert symbol_objects[1].symbol == "{U}"

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response("symbology/all.json")
        _symbols = All()

        assert "api.scryfall.com/symbology" in mock_urlopen.calls[0]["url"]


class TestParseMana:
    """Test ParseMana endpoint."""

    def test_parse_monocolored_cost(self, mock_urlopen):
        """Test parsing a monocolored mana cost."""
        mock_urlopen.set_response("symbology/parse_mana.json")
        parsed = ParseMana(cost="{2}{U}{U}")

        assert parsed.object == "mana_cost"
        assert parsed.cost == "{2}{U}{U}"
        assert parsed.mana_value == 4.0
        assert parsed.colors == ["U"]
        assert parsed.monocolored is True
        assert parsed.multicolored is False
        assert parsed.colorless is False

    def test_parse_multicolored_cost(self, mock_urlopen):
        """Test parsing a multicolored mana cost."""
        mock_urlopen.set_response("symbology/parse_mana_multicolor.json")
        parsed = ParseMana(cost="{G}{W}")

        assert parsed.object == "mana_cost"
        assert parsed.cost == "{G}{W}"
        assert parsed.mana_value == 2.0
        assert parsed.colors == ["G", "W"]
        assert parsed.monocolored is False
        assert parsed.multicolored is True
        assert parsed.colorless is False

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response("symbology/parse_mana.json")
        _parsed = ParseMana(cost="{2}{U}{U}")

        assert "api.scryfall.com/symbology/parse-mana" in mock_urlopen.calls[0]["url"]
        assert "cost=%7B2%7D%7BU%7D%7BU%7D" in mock_urlopen.calls[0]["url"]


class TestSymbologyMixins:
    """Test symbology data accessor mixins."""

    def test_symbology_object_mixin_properties(self, mock_urlopen):
        """Test that symbol properties are accessible."""
        mock_urlopen.set_response("symbology/all.json")
        symbols = All()

        symbol_objects = symbols.data
        white_symbol = symbol_objects[0]

        assert white_symbol.object == "card_symbol"
        assert white_symbol.symbol == "{W}"
        assert white_symbol.english == "one white mana"
        assert white_symbol.represents_mana is True
        assert white_symbol.mana_value == 1.0
        assert white_symbol.appears_in_mana_costs is True
        assert white_symbol.funny is False
        assert white_symbol.colors == ["W"]
        assert white_symbol.hybrid is False
        assert white_symbol.phyrexian is False

    def test_hybrid_symbol_properties(self, mock_urlopen):
        """Test that hybrid symbol properties work correctly."""
        mock_urlopen.set_response("symbology/all.json")
        symbols = All()

        symbol_objects = symbols.data
        hybrid_symbol = symbol_objects[2]  # {U/B}

        assert hybrid_symbol.symbol == "{U/B}"
        assert hybrid_symbol.english == "one blue or black mana"
        assert hybrid_symbol.hybrid is True
        assert hybrid_symbol.colors == ["U", "B"]

    def test_non_mana_symbol_properties(self, mock_urlopen):
        """Test that non-mana symbols have correct properties."""
        mock_urlopen.set_response("symbology/all.json")
        symbols = All()

        symbol_objects = symbols.data
        tap_symbol = symbol_objects[3]  # {T}

        assert tap_symbol.symbol == "{T}"
        assert tap_symbol.english == "tap this permanent"
        assert tap_symbol.represents_mana is False
        assert tap_symbol.appears_in_mana_costs is False
        assert tap_symbol.colors == []

    def test_mana_cost_mixin_properties(self, mock_urlopen):
        """Test that mana cost properties are accessible."""
        mock_urlopen.set_response("symbology/parse_mana.json")
        parsed = ParseMana(cost="{2}{U}{U}")

        assert parsed.object == "mana_cost"
        assert parsed.cost == "{2}{U}{U}"
        assert parsed.cmc == 4.0
        assert parsed.mana_value == 4.0
        assert parsed.colors == ["U"]
        assert parsed.colorless is False
        assert parsed.monocolored is True
        assert parsed.multicolored is False

    def test_filter_symbols_by_property(self, mock_urlopen):
        """Test filtering symbols by various properties."""
        mock_urlopen.set_response("symbology/all.json")
        symbols = All()

        # Filter to mana symbols
        mana_symbols = [s for s in symbols.data if s.represents_mana]
        assert len(mana_symbols) == 3

        # Filter to hybrid symbols
        hybrid_symbols = [s for s in symbols.data if s.hybrid]
        assert len(hybrid_symbols) == 1
        assert hybrid_symbols[0].symbol == "{U/B}"


class TestSymbologyFactory:
    """Test Symbology smart factory."""

    def test_factory_routes_to_all(self, mock_urlopen):
        """Test that factory routes to All when no parameters given."""
        mock_urlopen.set_response("symbology/all.json")
        symbols = Symbology()

        assert isinstance(symbols, All)
        assert "api.scryfall.com/symbology" in mock_urlopen.calls[0]["url"]

    def test_factory_routes_to_parse_mana(self, mock_urlopen):
        """Test that factory routes to ParseMana when given cost parameter."""
        mock_urlopen.set_response("symbology/parse_mana.json")
        parsed = Symbology(cost="{2}{U}{U}")

        assert isinstance(parsed, ParseMana)
        assert "api.scryfall.com/symbology/parse-mana" in mock_urlopen.calls[0]["url"]
        assert "cost=%7B2%7D%7BU%7D%7BU%7D" in mock_urlopen.calls[0]["url"]
