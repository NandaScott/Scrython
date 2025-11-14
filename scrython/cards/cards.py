from ..base import ScrythonRequestHandler
from ..base_mixins import ScryfallCatalogMixin, ScryfallListMixin
from .cards_mixins import CardsObjectMixin


class Object(CardsObjectMixin):
    """
    Wrapper class for individual card objects from Scryfall API responses.

    Provides access to all card properties through mixins (Core, Gameplay, Print fields).
    """

    def __init__(self, data):
        self._scryfall_data = data

    def __repr__(self) -> str:
        """
        Developer-friendly representation showing class name and key identifiers.

        Returns a string in the format: Object(id='...', name='...')

        Example:
            Object(id='bd8fa327-dd41-4737-8f19-2cf5eb1f7cdd', name='Lightning Bolt')
        """
        obj_id = self._scryfall_data.get("id")
        name = self._scryfall_data.get("name")

        parts = [f"id='{obj_id}'"] if obj_id else []
        if name:
            parts.append(f"name='{name}'")

        return f"Object({', '.join(parts)})"

    def __str__(self) -> str:
        """
        User-friendly string representation.

        Returns "Card Name (SET)" format

        Example:
            "Lightning Bolt (LEA)"
        """
        name = self._scryfall_data.get("name", "")
        set_code = self._scryfall_data.get("set", "").upper()
        return f"{name} ({set_code})" if set_code else name

    def __eq__(self, other: object) -> bool:
        """
        Compare card objects by their Scryfall ID.

        Args:
            other: Another object to compare with

        Returns:
            True if objects have the same Scryfall ID, False otherwise
        """
        if not isinstance(other, Object):
            return False

        self_id = self._scryfall_data.get("id")
        other_id = other._scryfall_data.get("id")

        if self_id and other_id:
            return self_id == other_id

        return self is other

    def __hash__(self) -> int:
        """
        Generate hash based on Scryfall ID to enable use in sets and dicts.

        Returns:
            Hash of the Scryfall ID
        """
        obj_id = self._scryfall_data.get("id")
        if obj_id:
            return hash(obj_id)

        return hash(id(self))

    def to_dict(self) -> dict:
        """
        Export card data as a dictionary.

        Returns a copy of the internal Scryfall data dictionary.

        Returns:
            Dictionary containing all card data
        """
        return self._scryfall_data.copy()

    def to_json(self, **kwargs) -> str:
        """
        Export card data as a JSON string.

        Args:
            **kwargs: Additional arguments passed to json.dumps()

        Returns:
            JSON string representation of the card data
        """
        import json

        return json.dumps(self._scryfall_data, **kwargs)

    @classmethod
    def from_dict(cls, data: dict) -> "Object":
        """
        Construct an Object from a dictionary without making an API request.

        Args:
            data: Dictionary containing Scryfall card data

        Returns:
            Object instance populated with the provided data
        """
        return cls(data.copy())


class Search(ScryfallListMixin, ScrythonRequestHandler):
    """
    Search for Magic cards using Scryfall's fulltext search syntax.

    Endpoint: GET /cards/search

    Returns a list object containing Cards. Use Scryfall's comprehensive search syntax
    to find cards by name, text, type, color, set, and many other properties.

    Args:
        q: A fulltext search query in Scryfall's syntax (required).
        unique: Strategy for omitting duplicate cards (optional).
            Options: 'cards' (default), 'art', 'prints'
        order: Method to sort returned cards (optional).
            Options: 'name', 'set', 'released', 'rarity', 'color', 'usd', 'tix',
                     'eur', 'cmc', 'power', 'toughness', 'edhrec', 'penny', 'artist', 'review'
        dir: Direction to sort (optional).
            Options: 'auto' (default), 'asc', 'desc'
        include_extras: Include extra cards like tokens (optional, default: false)
        include_multilingual: Include non-English cards (optional, default: false)
        include_variations: Include variations (optional, default: false)

    Example:
        # Search for red instants
        results = scrython.cards.Search(q='c:red type:instant')

        # Access results
        for card in results.data:
            print(card.name)

        # Check pagination
        if results.has_more:
            print(f"Total cards: {results.total_cards}")

    See: https://scryfall.com/docs/api/cards/search
    """

    _endpoint = "/cards/search"
    list_data_type = Object


class Named(CardsObjectMixin, ScrythonRequestHandler):
    """
    Get a single card by name using fuzzy or exact matching.

    Endpoint: GET /cards/named

    Returns a single Card object. Use fuzzy matching for typo tolerance or exact
    matching for precise lookups. This is faster than full search when you know
    the card name.

    Args:
        fuzzy: A fuzzy card name to search for (optional, mutually exclusive with exact).
        exact: The exact card name to search for (optional, mutually exclusive with fuzzy).
        set: A set code to limit the search to a specific set (optional).

    Example:
        # Fuzzy search (handles typos)
        card = scrython.cards.Named(fuzzy='Light Bolt')
        print(card.name)  # "Lightning Bolt"

        # Exact search
        card = scrython.cards.Named(exact='Black Lotus')
        print(card.prices)

    See: https://scryfall.com/docs/api/cards/named
    """

    _endpoint = "/cards/named"


class Autocomplete(ScryfallCatalogMixin, ScrythonRequestHandler):
    """
    Get card name autocomplete suggestions.

    Endpoint: GET /cards/autocomplete

    Returns a Catalog object containing up to 20 card name suggestions. Useful for
    building search interfaces with typeahead functionality.

    Args:
        q: The search prefix to autocomplete (required, minimum 2 characters).
        include_extras: Include extra cards like tokens (optional, default: false).

    Example:
        # Get suggestions for "light"
        suggestions = scrython.cards.Autocomplete(q='light')

        # Print all suggestions
        for name in suggestions.data:
            print(name)
        # Output: "Light", "Lightning Bolt", "Lightning Strike", ...

    See: https://scryfall.com/docs/api/cards/autocomplete
    """

    _endpoint = "/cards/autocomplete"


class Random(CardsObjectMixin, ScrythonRequestHandler):
    """
    Get a random card from Scryfall's database.

    Endpoint: GET /cards/random

    Returns a single random Card object. You can optionally provide a search query
    to get a random card matching specific criteria.

    Args:
        q: An optional fulltext search query to filter random results (optional).

    Example:
        # Get any random card
        card = scrython.cards.Random()
        print(f"Random card: {card.name}")

        # Get random mythic rare
        card = scrython.cards.Random(q='rarity:mythic')
        print(f"Random mythic: {card.name}")

    See: https://scryfall.com/docs/api/cards/random
    """

    _endpoint = "/cards/random"


class Collection(ScryfallListMixin, ScrythonRequestHandler):
    """
    Fetch a collection of cards by their identifiers.

    Endpoint: POST /cards/collection

    Returns a list of Card objects matching the provided identifiers. Accepts up to
    75 card identifiers per request. Useful for fetching specific cards in bulk.

    Args:
        data: A dict with 'identifiers' key containing a list of identifier dicts.
            Each identifier dict can contain: id, mtgo_id, multiverse_id, oracle_id,
            illustration_id, name, set+collector_number, etc.

    Example:
        # Fetch multiple cards by ID
        identifiers = [
            {'id': '5f8287b1-5bb6-4e8f-9d78-8f3e3b3e1c6d'},
            {'name': 'Lightning Bolt', 'set': 'lea'},
            {'multiverse_id': 409574}
        ]
        cards = scrython.cards.Collection(data={'identifiers': identifiers})

        for card in cards.data:
            print(f"{card.name} - {card.set}")

    See: https://scryfall.com/docs/api/cards/collection
    """

    _endpoint = "/cards/collection"
    list_data_type = Object


class ByCodeNumber(CardsObjectMixin, ScrythonRequestHandler):
    """
    Get a card by its set code and collector number.

    Endpoint: GET /cards/:code/:number(/:lang?)

    Returns a single Card object. This is the most precise way to identify a specific
    printing of a card. Optionally specify a language code for non-English printings.

    Args:
        code: The three-to-five-letter set code (required).
        number: The collector number (required, can include letters like "123a").
        lang: The 2-3 character language code (optional, default: 'en').

    Example:
        # Get a specific card from a set
        card = scrython.cards.ByCodeNumber(code='znr', number='123')
        print(f"{card.name} from {card.set_name}")

        # Get Japanese printing
        card = scrython.cards.ByCodeNumber(code='m21', number='123', lang='ja')

    See: https://scryfall.com/docs/api/cards/collector
    """

    _endpoint = "/cards/:code/:number/:lang?"


class ByMultiverseId(CardsObjectMixin, ScrythonRequestHandler):
    """
    Get a card by its Multiverse ID.

    Endpoint: GET /cards/multiverse/:id

    Returns a single Card object. Multiverse IDs are Gatherer's identifiers for card
    printings. Not all cards have Multiverse IDs (e.g., promo cards, tokens).

    Args:
        id: The Multiverse ID (required).

    Example:
        card = scrython.cards.ByMultiverseId(id=456789)
        print(f"{card.name} - Multiverse ID: {card.multiverse_ids}")

    See: https://scryfall.com/docs/api/cards/multiverse
    """

    _endpoint = "/cards/multiverse/:id"


class ByMTGOId(CardsObjectMixin, ScrythonRequestHandler):
    """
    Get a card by its Magic Online (MTGO) ID.

    Endpoint: GET /cards/mtgo/:id

    Returns a single Card object. MTGO IDs identify card objects in Magic Online's
    database. Not all cards are available on MTGO.

    Args:
        id: The MTGO ID (required).

    Example:
        card = scrython.cards.ByMTGOId(id=67890)
        print(f"{card.name} - MTGO ID: {card.mtgo_id}")

    See: https://scryfall.com/docs/api/cards/mtgo
    """

    _endpoint = "/cards/mtgo/:id"


class ByArenaId(CardsObjectMixin, ScrythonRequestHandler):
    """
    Get a card by its Arena ID.

    Endpoint: GET /cards/arena/:id

    Returns a single Card object. Arena IDs identify card objects in MTG Arena's
    database. Not all cards are available on Arena.

    Args:
        id: The Arena ID (required).

    Example:
        card = scrython.cards.ByArenaId(id=54321)
        print(f"{card.name} - Arena ID: {card.arena_id}")

    See: https://scryfall.com/docs/api/cards/arena
    """

    _endpoint = "/cards/arena/:id"


class ByTCGPlayerId(CardsObjectMixin, ScrythonRequestHandler):
    """
    Get a card by its TCGPlayer product ID.

    Endpoint: GET /cards/tcgplayer/:id

    Returns a single Card object. TCGPlayer IDs identify products on TCGPlayer's
    marketplace. Useful for price integration and marketplace linking.

    Args:
        id: The TCGPlayer ID (required).

    Example:
        card = scrython.cards.ByTCGPlayerId(id=98765)
        print(f"{card.name} - Price: ${card.prices['usd']}")

    See: https://scryfall.com/docs/api/cards/tcgplayer
    """

    _endpoint = "/cards/tcgplayer/:id"


class ByCardMarketId(CardsObjectMixin, ScrythonRequestHandler):
    """
    Get a card by its Cardmarket (formerly MKM) product ID.

    Endpoint: GET /cards/cardmarket/:id

    Returns a single Card object. Cardmarket IDs identify products on Cardmarket's
    European marketplace. Useful for EUR price integration.

    Args:
        id: The Cardmarket product ID (required).

    Example:
        card = scrython.cards.ByCardMarketId(id=11111)
        print(f"{card.name} - EUR Price: €{card.prices['eur']}")

    See: https://scryfall.com/docs/api/cards/cardmarket
    """

    _endpoint = "/cards/cardmarket/:id"


class ById(CardsObjectMixin, ScrythonRequestHandler):
    """
    Get a card by its Scryfall ID.

    Endpoint: GET /cards/:id

    Returns a single Card object. Scryfall IDs are unique UUIDs that identify specific
    printings in Scryfall's database. This is the canonical way to retrieve cards.

    Args:
        id: The Scryfall UUID (required).

    Example:
        card = scrython.cards.ById(id='5f8287b1-5bb6-4e8f-9d78-8f3e3b3e1c6d')
        print(f"{card.name} - {card.set_name}")

    See: https://scryfall.com/docs/api/cards/id
    """

    _endpoint = "/cards/:id"
