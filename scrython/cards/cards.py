from .cards_mixins import CoreFieldsMixin, GameplayFieldsMixin, PrintFieldsMixin, CardsObjectMixin
from ..base_mixins import ScryfallListMixin, ScryfallCatalogMixin
from ..base import ScrythonRequestHandler

class CardsObject(CardsObjectMixin):
  """
  Wrapper class for individual card objects from Scryfall API responses.

  Provides access to all card properties through mixins (Core, Gameplay, Print fields).
  """
  def __init__(self, data):
    self.scryfall_data = data

class CardsSearch(ScryfallListMixin, ScrythonRequestHandler):
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
      results = scrython.cards.CardsSearch(q='c:red type:instant')

      # Access results
      for card in results.data:
          print(card.name)

      # Check pagination
      if results.has_more:
          print(f"Total cards: {results.total_cards}")

  See: https://scryfall.com/docs/api/cards/search
  """
  _endpoint = '/cards/search'
  list_data_type = CardsObject

class CardsNamed(CardsObjectMixin, ScrythonRequestHandler):
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
      card = scrython.cards.CardsNamed(fuzzy='Light Bolt')
      print(card.name)  # "Lightning Bolt"

      # Exact search
      card = scrython.cards.CardsNamed(exact='Black Lotus')
      print(card.prices)

  See: https://scryfall.com/docs/api/cards/named
  """
  _endpoint = '/cards/named'

class CardsAutocomplete(ScryfallCatalogMixin, ScrythonRequestHandler):
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
      suggestions = scrython.cards.CardsAutocomplete(q='light')

      # Print all suggestions
      for name in suggestions.data:
          print(name)
      # Output: "Light", "Lightning Bolt", "Lightning Strike", ...

  See: https://scryfall.com/docs/api/cards/autocomplete
  """
  _endpoint = '/cards/autocomplete'

class CardsRandom(CardsObjectMixin, ScrythonRequestHandler):
  """
  Get a random card from Scryfall's database.

  Endpoint: GET /cards/random

  Returns a single random Card object. You can optionally provide a search query
  to get a random card matching specific criteria.

  Args:
      q: An optional fulltext search query to filter random results (optional).

  Example:
      # Get any random card
      card = scrython.cards.CardsRandom()
      print(f"Random card: {card.name}")

      # Get random mythic rare
      card = scrython.cards.CardsRandom(q='rarity:mythic')
      print(f"Random mythic: {card.name}")

  See: https://scryfall.com/docs/api/cards/random
  """
  _endpoint = '/cards/random'

class CardsCollection(ScryfallListMixin, ScrythonRequestHandler):
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
      cards = scrython.cards.CardsCollection(data={'identifiers': identifiers})

      for card in cards.data:
          print(f"{card.name} - {card.set}")

  See: https://scryfall.com/docs/api/cards/collection
  """
  _endpoint = '/cards/collection'

class CardsByCodeNumber(CardsObjectMixin, ScrythonRequestHandler):
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
      card = scrython.cards.CardsByCodeNumber(code='znr', number='123')
      print(f"{card.name} from {card.set_name}")

      # Get Japanese printing
      card = scrython.cards.CardsByCodeNumber(code='m21', number='123', lang='ja')

  See: https://scryfall.com/docs/api/cards/collector
  """
  _endpoint = '/cards/:code/:number/:lang?'

class CardsByMultiverseId(CardsObjectMixin, ScrythonRequestHandler):
  """
  Get a card by its Multiverse ID.

  Endpoint: GET /cards/multiverse/:id

  Returns a single Card object. Multiverse IDs are Gatherer's identifiers for card
  printings. Not all cards have Multiverse IDs (e.g., promo cards, tokens).

  Args:
      id: The Multiverse ID (required).

  Example:
      card = scrython.cards.CardsByMultiverseId(id=456789)
      print(f"{card.name} - Multiverse ID: {card.multiverse_ids}")

  See: https://scryfall.com/docs/api/cards/multiverse
  """
  _endpoint = '/cards/multiverse/:id'

class CardsByMTGOId(CardsObjectMixin, ScrythonRequestHandler):
  """
  Get a card by its Magic Online (MTGO) ID.

  Endpoint: GET /cards/mtgo/:id

  Returns a single Card object. MTGO IDs identify card objects in Magic Online's
  database. Not all cards are available on MTGO.

  Args:
      id: The MTGO ID (required).

  Example:
      card = scrython.cards.CardsByMTGOId(id=67890)
      print(f"{card.name} - MTGO ID: {card.mtgo_id}")

  See: https://scryfall.com/docs/api/cards/mtgo
  """
  _endpoint = '/cards/mtgo/:id'

class CardsByArenaId(CardsObjectMixin, ScrythonRequestHandler):
  """
  Get a card by its Arena ID.

  Endpoint: GET /cards/arena/:id

  Returns a single Card object. Arena IDs identify card objects in MTG Arena's
  database. Not all cards are available on Arena.

  Args:
      id: The Arena ID (required).

  Example:
      card = scrython.cards.CardsByArenaId(id=54321)
      print(f"{card.name} - Arena ID: {card.arena_id}")

  See: https://scryfall.com/docs/api/cards/arena
  """
  _endpoint = '/cards/arena/:id'

class CardsByTCGPlayerId(CardsObjectMixin, ScrythonRequestHandler):
  """
  Get a card by its TCGPlayer product ID.

  Endpoint: GET /cards/tcgplayer/:id

  Returns a single Card object. TCGPlayer IDs identify products on TCGPlayer's
  marketplace. Useful for price integration and marketplace linking.

  Args:
      id: The TCGPlayer ID (required).

  Example:
      card = scrython.cards.CardsByTCGPlayerId(id=98765)
      print(f"{card.name} - Price: ${card.prices['usd']}")

  See: https://scryfall.com/docs/api/cards/tcgplayer
  """
  _endpoint = '/cards/tcgplayer/:id'

class CardsByCardMarketId(CardsObjectMixin, ScrythonRequestHandler):
  """
  Get a card by its Cardmarket (formerly MKM) product ID.

  Endpoint: GET /cards/cardmarket/:id

  Returns a single Card object. Cardmarket IDs identify products on Cardmarket's
  European marketplace. Useful for EUR price integration.

  Args:
      id: The Cardmarket product ID (required).

  Example:
      card = scrython.cards.CardsByCardMarketId(id=11111)
      print(f"{card.name} - EUR Price: €{card.prices['eur']}")

  See: https://scryfall.com/docs/api/cards/cardmarket
  """
  _endpoint = '/cards/cardmarket/:id'

class CardsById(CardsObjectMixin, ScrythonRequestHandler):
  """
  Get a card by its Scryfall ID.

  Endpoint: GET /cards/:id

  Returns a single Card object. Scryfall IDs are unique UUIDs that identify specific
  printings in Scryfall's database. This is the canonical way to retrieve cards.

  Args:
      id: The Scryfall UUID (required).

  Example:
      card = scrython.cards.CardsById(id='5f8287b1-5bb6-4e8f-9d78-8f3e3b3e1c6d')
      print(f"{card.name} - {card.set_name}")

  See: https://scryfall.com/docs/api/cards/id
  """
  _endpoint = '/cards/:id'

class Cards:
  """
  Smart factory for accessing all Scryfall card endpoints.

  This factory routes to the appropriate endpoint class based on the parameters
  provided. Use this instead of importing individual endpoint classes directly
  for a more convenient API.

  Supported Modes:

      Named Lookup (fuzzy or exact match):
          card = Cards(fuzzy='Lightning Bolt')
          card = Cards(exact='Lightning Bolt')

      Search with Scryfall syntax:
          results = Cards(search='c:red cmc:1')

      Autocomplete:
          suggestions = Cards(autocomplete='light')

      Random card:
          card = Cards(random=True)
          card = Cards(random=True, q='rarity:mythic')

      Multiple cards by identifier:
          cards = Cards(collection=[
              {'name': 'Lightning Bolt'},
              {'id': 'card-uuid-here'}
          ])

      By set code and collector number:
          card = Cards(code='m21', number='123')
          card = Cards(code='m21', number='123', lang='ja')

      By various IDs:
          card = Cards(id='scryfall-uuid')
          card = Cards(multiverse='12345')
          card = Cards(mtgo='67890')
          card = Cards(arena='54321')
          card = Cards(tcgplayer='98765')
          card = Cards(cardmarket='11111')

  Returns:
      An instance of the appropriate endpoint class (CardsNamed, CardsSearch, etc.)
      based on the parameters provided.

  Raises:
      ValueError: If no valid parameters are provided.

  Example:
      import scrython

      # Fuzzy search
      card = scrython.Cards(fuzzy='Light Bolt')
      print(card.name)  # "Lightning Bolt"

      # Search
      results = scrython.Cards(search='type:creature cmc:1')
      for card in results.data:
          print(card.name)

      # By set and number
      card = scrython.Cards(code='znr', number='123')

  See: https://scryfall.com/docs/api/cards
  """
  def __new__(self, **kwargs):
    if search := kwargs.get('search', None):
      return CardsSearch(q=search, **kwargs)

    if kwargs.get('fuzzy', None):
      return CardsNamed(**kwargs)
    elif kwargs.get('exact', None):
      return CardsNamed(**kwargs)

    if autocomplete := kwargs.get('autocomplete', None):
      return CardsAutocomplete(q=autocomplete, **kwargs)

    if kwargs.get('random', None):
      return CardsRandom(**kwargs)

    if identifiers := kwargs.get('collection', None):
      return CardsCollection(data={'identifiers': identifiers}, **kwargs)

    if kwargs.get('code', None) or kwargs.get('number', None):
      return CardsByCodeNumber(**kwargs)

    if multiverse := kwargs.get('multiverse', None):
      return CardsByMultiverseId(id=multiverse, **kwargs)

    if mtgo := kwargs.get('mtgo', None):
      return CardsByMTGOId(id=mtgo, **kwargs)

    if arena := kwargs.get('arena', None):
      return CardsByArenaId(id=arena, **kwargs)

    if tcgplayer := kwargs.get('tcgplayer', None):
      return CardsByTCGPlayerId(id=tcgplayer, **kwargs)

    if cardmarket := kwargs.get('cardmarket', None):
      return CardsByCardMarketId(id=cardmarket, **kwargs)

    if kwargs.get('id', None):
      return CardsById(**kwargs)

    raise ValueError(
      "No valid parameters provided to Cards factory.\n"
      "Use one of the following:\n"
      "  - fuzzy='name' or exact='name' - Get card by name\n"
      "  - search='query' - Search with Scryfall syntax\n"
      "  - autocomplete='text' - Get name suggestions\n"
      "  - random=True - Get random card\n"
      "  - collection=[identifiers] - Get multiple cards\n"
      "  - code='set', number='num' - Get by set and collector number\n"
      "  - multiverse='id' - Get by Multiverse ID\n"
      "  - mtgo='id' - Get by MTGO ID\n"
      "  - arena='id' - Get by Arena ID\n"
      "  - tcgplayer='id' - Get by TCGPlayer ID\n"
      "  - cardmarket='id' - Get by Cardmarket ID\n"
      "  - id='uuid' - Get by Scryfall ID\n"
      "See https://scryfall.com/docs/api/cards for details."
    )
