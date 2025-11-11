"""Tests for scrython.cards module."""

import pytest

from scrython.cards import (
    Autocomplete,
    ByArenaId,
    ByCardMarketId,
    ByCodeNumber,
    ById,
    ByMTGOId,
    ByMultiverseId,
    ByTCGPlayerId,
    Collection,
    Named,
    Random,
    Search,
)


class TestNamed:
    """Test Named endpoint."""

    def test_fuzzy_search(self, mock_urlopen):
        """Test fuzzy search for a card."""
        mock_urlopen.set_response("cards/named.json")
        card = Named(fuzzy="Black Lotus")

        assert card.scryfall_data.name == "Black Lotus"
        assert "fuzzy=Black+Lotus" in mock_urlopen.calls[0]["url"]

    def test_exact_search(self, mock_urlopen):
        """Test exact search for a card."""
        mock_urlopen.set_response("cards/named.json")
        card = Named(exact="Black Lotus")

        assert card.scryfall_data.name == "Black Lotus"
        assert "exact=Black+Lotus" in mock_urlopen.calls[0]["url"]

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response("cards/named.json")
        _card = Named(fuzzy="test")

        assert "api.scryfall.com/cards/named" in mock_urlopen.calls[0]["url"]


class TestSearch:
    """Test Search endpoint."""

    def test_search_query(self, mock_urlopen):
        """Test searching with a query."""
        mock_urlopen.set_response("cards/search.json")
        results = Search(q="lightning")

        assert results.scryfall_data.object == "list"
        assert results.scryfall_data.total_cards == 2
        assert "q=lightning" in mock_urlopen.calls[0]["url"]

    def test_list_mixin_data_method(self, mock_urlopen):
        """Test that list mixin provides data property."""
        mock_urlopen.set_response("cards/search.json")
        results = Search(q="lightning")

        cards = results.data
        assert len(cards) == 2
        assert cards[0].name == "Lightning Bolt"

    def test_list_mixin_has_more(self, mock_urlopen):
        """Test has_more property from list mixin."""
        mock_urlopen.set_response("cards/search.json")
        results = Search(q="lightning")

        assert results.has_more is False

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response("cards/search.json")
        _results = Search(q="test")

        assert "api.scryfall.com/cards/search" in mock_urlopen.calls[0]["url"]


class TestAutocomplete:
    """Test Autocomplete endpoint."""

    def test_autocomplete_query(self, mock_urlopen):
        """Test autocomplete suggestions."""
        mock_urlopen.set_response("cards/autocomplete.json")
        results = Autocomplete(q="Black")

        assert results.scryfall_data.object == "catalog"
        assert results.scryfall_data.total_values == 5
        assert "q=Black" in mock_urlopen.calls[0]["url"]

    def test_catalog_mixin_data_method(self, mock_urlopen):
        """Test that catalog mixin provides data property."""
        mock_urlopen.set_response("cards/autocomplete.json")
        results = Autocomplete(q="Black")

        suggestions = results.data
        assert len(suggestions) == 5
        assert "Black Lotus" in suggestions

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response("cards/autocomplete.json")
        _results = Autocomplete(q="test")

        assert "api.scryfall.com/cards/autocomplete" in mock_urlopen.calls[0]["url"]


class TestRandom:
    """Test Random endpoint."""

    def test_random_card(self, mock_urlopen):
        """Test getting a random card."""
        mock_urlopen.set_response("cards/random.json")
        card = Random()

        assert card.scryfall_data.object == "card"
        assert card.scryfall_data.name == "Forest"

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response("cards/random.json")
        _card = Random()

        assert "api.scryfall.com/cards/random" in mock_urlopen.calls[0]["url"]


class TestCollection:
    """Test Collection endpoint."""

    def test_collection_with_identifiers(self, mock_urlopen, sample_list_response, sample_card):
        """Test getting a collection of cards by identifiers."""
        sample_list_response["data"] = [sample_card]
        mock_urlopen.set_response(data=sample_list_response)

        identifiers = [{"id": "f4fa7d2c-3d02-4a5e-8b4d-2e4e3e7f8c9a"}, {"name": "Lightning Bolt"}]
        collection = Collection(data={"identifiers": identifiers})

        assert collection.scryfall_data.object == "list"
        assert len(collection.data) == 1

    def test_endpoint_path(self, mock_urlopen, sample_list_response):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response(data=sample_list_response)
        _collection = Collection(data={"identifiers": []})

        assert "api.scryfall.com/cards/collection" in mock_urlopen.calls[0]["url"]


class TestByCodeNumber:
    """Test ByCodeNumber endpoint."""

    def test_get_card_by_code_and_number(self, mock_urlopen):
        """Test getting a card by set code and collector number."""
        mock_urlopen.set_response("cards/named.json")
        card = ByCodeNumber(code="lea", number="232")

        assert card.scryfall_data.object == "card"
        assert "api.scryfall.com/cards/lea/232" in mock_urlopen.calls[0]["url"]

    def test_with_language_param(self, mock_urlopen):
        """Test getting a card with language parameter."""
        mock_urlopen.set_response("cards/named.json")
        _card = ByCodeNumber(code="lea", number="232", lang="en")

        assert "lang=en" in mock_urlopen.calls[0]["url"]

    def test_missing_required_params(self, mock_urlopen):
        """Test that missing required parameters raise error."""
        mock_urlopen.set_response("cards/named.json")

        with pytest.raises(KeyError):
            ByCodeNumber(code="lea")  # Missing number


class TestByMultiverseId:
    """Test ByMultiverseId endpoint."""

    def test_get_card_by_multiverse_id(self, mock_urlopen):
        """Test getting a card by Multiverse ID."""
        mock_urlopen.set_response("cards/named.json")
        card = ByMultiverseId(id="600")

        assert card.scryfall_data.object == "card"
        assert "api.scryfall.com/cards/multiverse/600" in mock_urlopen.calls[0]["url"]


class TestByMTGOId:
    """Test ByMTGOId endpoint."""

    def test_get_card_by_mtgo_id(self, mock_urlopen):
        """Test getting a card by MTGO ID."""
        mock_urlopen.set_response("cards/named.json")
        card = ByMTGOId(id="12345")

        assert card.scryfall_data.object == "card"
        assert "api.scryfall.com/cards/mtgo/12345" in mock_urlopen.calls[0]["url"]


class TestByArenaId:
    """Test ByArenaId endpoint."""

    def test_get_card_by_arena_id(self, mock_urlopen):
        """Test getting a card by Arena ID."""
        mock_urlopen.set_response("cards/named.json")
        card = ByArenaId(id="67890")

        assert card.scryfall_data.object == "card"
        assert "api.scryfall.com/cards/arena/67890" in mock_urlopen.calls[0]["url"]


class TestByTCGPlayerId:
    """Test ByTCGPlayerId endpoint."""

    def test_get_card_by_tcgplayer_id(self, mock_urlopen):
        """Test getting a card by TCGPlayer ID."""
        mock_urlopen.set_response("cards/named.json")
        card = ByTCGPlayerId(id="11111")

        assert card.scryfall_data.object == "card"
        assert "api.scryfall.com/cards/tcgplayer/11111" in mock_urlopen.calls[0]["url"]


class TestByCardMarketId:
    """Test ByCardMarketId endpoint."""

    def test_get_card_by_cardmarket_id(self, mock_urlopen):
        """Test getting a card by CardMarket ID."""
        mock_urlopen.set_response("cards/named.json")
        card = ByCardMarketId(id="22222")

        assert card.scryfall_data.object == "card"
        assert "api.scryfall.com/cards/cardmarket/22222" in mock_urlopen.calls[0]["url"]


class TestById:
    """Test ById endpoint."""

    def test_get_card_by_id(self, mock_urlopen):
        """Test getting a card by Scryfall ID."""
        mock_urlopen.set_response("cards/named.json")
        card = ById(id="bd8fa327-dd41-4737-8f19-2cf5eb1f7cdd")

        assert card.scryfall_data.object == "card"
        assert (
            "api.scryfall.com/cards/bd8fa327-dd41-4737-8f19-2cf5eb1f7cdd"
            in mock_urlopen.calls[0]["url"]
        )


class TestCardsMixins:
    """Test card data accessor mixins."""

    def test_core_fields_mixin(self, mock_urlopen):
        """Test that core card fields are accessible."""
        mock_urlopen.set_response("cards/named.json")
        card = Named(fuzzy="Black Lotus")

        assert card.name == "Black Lotus"
        assert card.cmc == 0.0
        assert card.type_line == "Artifact"
        assert card.oracle_text == "{T}, Sacrifice Black Lotus: Add three mana of any one color."

    def test_gameplay_fields_mixin(self, mock_urlopen):
        """Test that gameplay fields are accessible."""
        mock_urlopen.set_response("cards/named.json")
        card = Named(fuzzy="Black Lotus")

        assert card.colors == []
        assert card.color_identity == []
        # Test legalities access
        assert hasattr(card, "legalities")

    def test_print_fields_mixin(self, mock_urlopen):
        """Test that print-specific fields are accessible."""
        mock_urlopen.set_response("cards/named.json")
        card = Named(fuzzy="Black Lotus")

        assert card.set == "lea"
        assert card.set_name == "Limited Edition Alpha"
        assert card.rarity == "rare"
        assert card.artist == "Christopher Rush"
