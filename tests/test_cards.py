"""Tests for scrython.cards module."""
import pytest
import scrython
from scrython.cards.cards import (
    CardsSearch, CardsNamed, CardsAutocomplete, CardsRandom, CardsCollection,
    CardsByCodeNumber, CardsByMultiverseId, CardsByMTGOId, CardsByArenaId,
    CardsByTCGPlayerId, CardsByCardMarketId, CardsById, Cards
)


class TestCardsNamed:
    """Test CardsNamed endpoint."""

    def test_fuzzy_search(self, mock_urlopen):
        """Test fuzzy search for a card."""
        mock_urlopen.set_response('cards/named.json')
        card = CardsNamed(fuzzy='Black Lotus')

        assert card.scryfall_data['name'] == 'Black Lotus'
        assert 'fuzzy=Black+Lotus' in mock_urlopen.calls[0]['url']

    def test_exact_search(self, mock_urlopen):
        """Test exact search for a card."""
        mock_urlopen.set_response('cards/named.json')
        card = CardsNamed(exact='Black Lotus')

        assert card.scryfall_data['name'] == 'Black Lotus'
        assert 'exact=Black+Lotus' in mock_urlopen.calls[0]['url']

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response('cards/named.json')
        card = CardsNamed(fuzzy='test')

        assert 'api.scryfall.com/cards/named' in mock_urlopen.calls[0]['url']


class TestCardsSearch:
    """Test CardsSearch endpoint."""

    def test_search_query(self, mock_urlopen):
        """Test searching with a query."""
        mock_urlopen.set_response('cards/search.json')
        results = CardsSearch(q='lightning')

        assert results.scryfall_data['object'] == 'list'
        assert results.scryfall_data['total_cards'] == 2
        assert 'q=lightning' in mock_urlopen.calls[0]['url']

    def test_list_mixin_data_method(self, mock_urlopen):
        """Test that list mixin provides data property."""
        mock_urlopen.set_response('cards/search.json')
        results = CardsSearch(q='lightning')

        cards = results.data
        assert len(cards) == 2
        assert cards[0].name == 'Lightning Bolt'

    def test_list_mixin_has_more(self, mock_urlopen):
        """Test has_more property from list mixin."""
        mock_urlopen.set_response('cards/search.json')
        results = CardsSearch(q='lightning')

        assert results.has_more is False

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response('cards/search.json')
        results = CardsSearch(q='test')

        assert 'api.scryfall.com/cards/search' in mock_urlopen.calls[0]['url']


class TestCardsAutocomplete:
    """Test CardsAutocomplete endpoint."""

    def test_autocomplete_query(self, mock_urlopen):
        """Test autocomplete suggestions."""
        mock_urlopen.set_response('cards/autocomplete.json')
        results = CardsAutocomplete(q='Black')

        assert results.scryfall_data['object'] == 'catalog'
        assert results.scryfall_data['total_values'] == 5
        assert 'q=Black' in mock_urlopen.calls[0]['url']

    def test_catalog_mixin_data_method(self, mock_urlopen):
        """Test that catalog mixin provides data property."""
        mock_urlopen.set_response('cards/autocomplete.json')
        results = CardsAutocomplete(q='Black')

        suggestions = results.data
        assert len(suggestions) == 5
        assert 'Black Lotus' in suggestions

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response('cards/autocomplete.json')
        results = CardsAutocomplete(q='test')

        assert 'api.scryfall.com/cards/autocomplete' in mock_urlopen.calls[0]['url']


class TestCardsRandom:
    """Test CardsRandom endpoint."""

    def test_random_card(self, mock_urlopen):
        """Test getting a random card."""
        mock_urlopen.set_response('cards/random.json')
        card = CardsRandom()

        assert card.scryfall_data['object'] == 'card'
        assert card.scryfall_data['name'] == 'Forest'

    def test_endpoint_path(self, mock_urlopen):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response('cards/random.json')
        card = CardsRandom()

        assert 'api.scryfall.com/cards/random' in mock_urlopen.calls[0]['url']


class TestCardsCollection:
    """Test CardsCollection endpoint."""

    def test_collection_with_identifiers(self, mock_urlopen, sample_list_response, sample_card):
        """Test getting a collection of cards by identifiers."""
        sample_list_response['data'] = [sample_card]
        mock_urlopen.set_response(data=sample_list_response)

        identifiers = [
            {'id': 'f4fa7d2c-3d02-4a5e-8b4d-2e4e3e7f8c9a'},
            {'name': 'Lightning Bolt'}
        ]
        collection = CardsCollection(data={'identifiers': identifiers})

        assert collection.scryfall_data['object'] == 'list'
        assert len(collection.data) == 1

    def test_endpoint_path(self, mock_urlopen, sample_list_response):
        """Test that the correct endpoint path is used."""
        mock_urlopen.set_response(data=sample_list_response)
        collection = CardsCollection(data={'identifiers': []})

        assert 'api.scryfall.com/cards/collection' in mock_urlopen.calls[0]['url']


class TestCardsByCodeNumber:
    """Test CardsByCodeNumber endpoint."""

    def test_get_card_by_code_and_number(self, mock_urlopen):
        """Test getting a card by set code and collector number."""
        mock_urlopen.set_response('cards/named.json')
        card = CardsByCodeNumber(code='lea', number='232')

        assert card.scryfall_data['object'] == 'card'
        assert 'api.scryfall.com/cards/lea/232' in mock_urlopen.calls[0]['url']

    def test_with_language_param(self, mock_urlopen):
        """Test getting a card with language parameter."""
        mock_urlopen.set_response('cards/named.json')
        card = CardsByCodeNumber(code='lea', number='232', lang='en')

        assert 'lang=en' in mock_urlopen.calls[0]['url']

    def test_missing_required_params(self, mock_urlopen):
        """Test that missing required parameters raise error."""
        mock_urlopen.set_response('cards/named.json')

        with pytest.raises(KeyError):
            CardsByCodeNumber(code='lea')  # Missing number


class TestCardsByMultiverseId:
    """Test CardsByMultiverseId endpoint."""

    def test_get_card_by_multiverse_id(self, mock_urlopen):
        """Test getting a card by Multiverse ID."""
        mock_urlopen.set_response('cards/named.json')
        card = CardsByMultiverseId(id='600')

        assert card.scryfall_data['object'] == 'card'
        assert 'api.scryfall.com/cards/multiverse/600' in mock_urlopen.calls[0]['url']


class TestCardsByMTGOId:
    """Test CardsByMTGOId endpoint."""

    def test_get_card_by_mtgo_id(self, mock_urlopen):
        """Test getting a card by MTGO ID."""
        mock_urlopen.set_response('cards/named.json')
        card = CardsByMTGOId(id='12345')

        assert card.scryfall_data['object'] == 'card'
        assert 'api.scryfall.com/cards/mtgo/12345' in mock_urlopen.calls[0]['url']


class TestCardsByArenaId:
    """Test CardsByArenaId endpoint."""

    def test_get_card_by_arena_id(self, mock_urlopen):
        """Test getting a card by Arena ID."""
        mock_urlopen.set_response('cards/named.json')
        card = CardsByArenaId(id='67890')

        assert card.scryfall_data['object'] == 'card'
        assert 'api.scryfall.com/cards/arena/67890' in mock_urlopen.calls[0]['url']


class TestCardsByTCGPlayerId:
    """Test CardsByTCGPlayerId endpoint."""

    def test_get_card_by_tcgplayer_id(self, mock_urlopen):
        """Test getting a card by TCGPlayer ID."""
        mock_urlopen.set_response('cards/named.json')
        card = CardsByTCGPlayerId(id='11111')

        assert card.scryfall_data['object'] == 'card'
        assert 'api.scryfall.com/cards/tcgplayer/11111' in mock_urlopen.calls[0]['url']


class TestCardsByCardMarketId:
    """Test CardsByCardMarketId endpoint."""

    def test_get_card_by_cardmarket_id(self, mock_urlopen):
        """Test getting a card by CardMarket ID."""
        mock_urlopen.set_response('cards/named.json')
        card = CardsByCardMarketId(id='22222')

        assert card.scryfall_data['object'] == 'card'
        assert 'api.scryfall.com/cards/cardmarket/22222' in mock_urlopen.calls[0]['url']


class TestCardsById:
    """Test CardsById endpoint."""

    def test_get_card_by_id(self, mock_urlopen):
        """Test getting a card by Scryfall ID."""
        mock_urlopen.set_response('cards/named.json')
        card = CardsById(id='bd8fa327-dd41-4737-8f19-2cf5eb1f7cdd')

        assert card.scryfall_data['object'] == 'card'
        assert 'api.scryfall.com/cards/bd8fa327-dd41-4737-8f19-2cf5eb1f7cdd' in mock_urlopen.calls[0]['url']


class TestCardsFactory:
    """Test the Cards factory class routing logic."""

    def test_factory_routes_search(self, mock_urlopen):
        """Test that Cards factory routes to CardsSearch."""
        mock_urlopen.set_response('cards/search.json')
        result = Cards(search='lightning')

        assert isinstance(result, CardsSearch)
        assert 'q=lightning' in mock_urlopen.calls[0]['url']

    def test_factory_routes_fuzzy(self, mock_urlopen):
        """Test that Cards factory routes to CardsNamed with fuzzy."""
        mock_urlopen.set_response('cards/named.json')
        result = Cards(fuzzy='Black Lotus')

        assert isinstance(result, CardsNamed)
        assert 'fuzzy=Black+Lotus' in mock_urlopen.calls[0]['url']

    def test_factory_routes_exact(self, mock_urlopen):
        """Test that Cards factory routes to CardsNamed with exact."""
        mock_urlopen.set_response('cards/named.json')
        result = Cards(exact='Black Lotus')

        assert isinstance(result, CardsNamed)
        assert 'exact=Black+Lotus' in mock_urlopen.calls[0]['url']

    def test_factory_routes_autocomplete(self, mock_urlopen):
        """Test that Cards factory routes to CardsAutocomplete."""
        mock_urlopen.set_response('cards/autocomplete.json')
        result = Cards(autocomplete='Black')

        assert isinstance(result, CardsAutocomplete)
        assert 'q=Black' in mock_urlopen.calls[0]['url']

    def test_factory_routes_random(self, mock_urlopen):
        """Test that Cards factory routes to CardsRandom."""
        mock_urlopen.set_response('cards/random.json')
        result = Cards(random=True)

        assert isinstance(result, CardsRandom)

    def test_factory_routes_collection(self, mock_urlopen, sample_list_response):
        """Test that Cards factory routes to CardsCollection."""
        mock_urlopen.set_response(data=sample_list_response)
        identifiers = [{'id': 'test'}]
        result = Cards(collection=identifiers)

        assert isinstance(result, CardsCollection)

    def test_factory_routes_code_number(self, mock_urlopen):
        """Test that Cards factory routes to CardsByCodeNumber."""
        mock_urlopen.set_response('cards/named.json')
        result = Cards(code='lea', number='232')

        assert isinstance(result, CardsByCodeNumber)

    def test_factory_routes_multiverse(self, mock_urlopen):
        """Test that Cards factory routes to CardsByMultiverseId."""
        mock_urlopen.set_response('cards/named.json')
        result = Cards(multiverse='600')

        assert isinstance(result, CardsByMultiverseId)

    def test_factory_routes_mtgo(self, mock_urlopen):
        """Test that Cards factory routes to CardsByMTGOId."""
        mock_urlopen.set_response('cards/named.json')
        result = Cards(mtgo='12345')

        assert isinstance(result, CardsByMTGOId)

    def test_factory_routes_arena(self, mock_urlopen):
        """Test that Cards factory routes to CardsByArenaId."""
        mock_urlopen.set_response('cards/named.json')
        result = Cards(arena='67890')

        assert isinstance(result, CardsByArenaId)

    def test_factory_routes_tcgplayer(self, mock_urlopen):
        """Test that Cards factory routes to CardsByTCGPlayerId."""
        mock_urlopen.set_response('cards/named.json')
        result = Cards(tcgplayer='11111')

        assert isinstance(result, CardsByTCGPlayerId)

    def test_factory_routes_cardmarket(self, mock_urlopen):
        """Test that Cards factory routes to CardsByCardMarketId."""
        mock_urlopen.set_response('cards/named.json')
        result = Cards(cardmarket='22222')

        assert isinstance(result, CardsByCardMarketId)

    def test_factory_routes_id(self, mock_urlopen):
        """Test that Cards factory routes to CardsById."""
        mock_urlopen.set_response('cards/named.json')
        result = Cards(id='bd8fa327-dd41-4737-8f19-2cf5eb1f7cdd')

        assert isinstance(result, CardsById)

    def test_factory_raises_error_no_mode(self):
        """Test that Cards factory raises error when no valid parameters provided."""
        with pytest.raises(Exception, match='No mode found'):
            Cards()


class TestCardsMixins:
    """Test card data accessor mixins."""

    def test_core_fields_mixin(self, mock_urlopen):
        """Test that core card fields are accessible."""
        mock_urlopen.set_response('cards/named.json')
        card = Cards(fuzzy='Black Lotus')

        assert card.name == 'Black Lotus'
        assert card.cmc == 0.0
        assert card.type_line == 'Artifact'
        assert card.oracle_text == '{T}, Sacrifice Black Lotus: Add three mana of any one color.'

    def test_gameplay_fields_mixin(self, mock_urlopen):
        """Test that gameplay fields are accessible."""
        mock_urlopen.set_response('cards/named.json')
        card = Cards(fuzzy='Black Lotus')

        assert card.colors == []
        assert card.color_identity == []
        # Test legalities access
        assert hasattr(card, 'legalities')

    def test_print_fields_mixin(self, mock_urlopen):
        """Test that print-specific fields are accessible."""
        mock_urlopen.set_response('cards/named.json')
        card = Cards(fuzzy='Black Lotus')

        assert card.set == 'lea'
        assert card.set_name == 'Limited Edition Alpha'
        assert card.rarity == 'rare'
        assert card.artist == 'Christopher Rush'
