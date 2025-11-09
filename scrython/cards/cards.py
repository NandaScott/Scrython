from .cards_mixins import CoreFieldsMixin, GameplayFieldsMixin, PrintFieldsMixin, CardsObjectMixin
from ..base_mixins import ScryfallListMixin, ScryfallCatalogMixin
from ..base import ScrythonRequestHandler

class CardsObject(CardsObjectMixin):
  def __init__(self, data):
    self.scryfall_data = data

class CardsSearch(ScryfallListMixin, ScrythonRequestHandler):
  _endpoint = '/cards/search'
  list_data_type = CardsObject

class CardsNamed(CardsObjectMixin, ScrythonRequestHandler):
  _endpoint = '/cards/named'

class CardsAutocomplete(ScryfallCatalogMixin, ScrythonRequestHandler):
  _endpoint = '/cards/autocomplete'

class CardsRandom(CardsObjectMixin, ScrythonRequestHandler):
  _endpoint = '/cards/random'

class CardsCollection(ScryfallListMixin, ScrythonRequestHandler):
  _endpoint = '/cards/collection'

class CardsByCodeNumber(CardsObjectMixin, ScrythonRequestHandler):
  _endpoint = '/cards/:code/:number/:lang?'

class CardsByMultiverseId(CardsObjectMixin, ScrythonRequestHandler):
  _endpoint = '/cards/multiverse/:id'

class CardsByMTGOId(CardsObjectMixin, ScrythonRequestHandler):
  _endpoint = '/cards/mtgo/:id'

class CardsByArenaId(CardsObjectMixin, ScrythonRequestHandler):
  _endpoint = '/cards/arena/:id'

class CardsByTCGPlayerId(CardsObjectMixin, ScrythonRequestHandler):
  _endpoint = '/cards/tcgplayer/:id'

class CardsByCardMarketId(CardsObjectMixin, ScrythonRequestHandler):
  _endpoint = '/cards/cardmarket/:id'

class CardsById(CardsObjectMixin, ScrythonRequestHandler):
  _endpoint = '/cards/:id'

class Cards:
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
