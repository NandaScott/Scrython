from scrython.base import ScrythonRequestHandler
from scrython.base_mixins import ScryfallListMixin
from .sets_mixins import SetsObjectMixin

class SetsObject(SetsObjectMixin):
  def __init__(self, data):
    self.scryfall_data = data

class AllSets(ScryfallListMixin, ScrythonRequestHandler):
  _endpoint = '/sets'
  list_data_type = SetsObject

class SetsByCode(SetsObjectMixin, ScrythonRequestHandler):
  _endpoint = '/sets/:code'

class SetsByTCGPlayerId(SetsObjectMixin, ScrythonRequestHandler):
  _endpoint = '/sets/tcgplayer/:id'

class SetsById(SetsObjectMixin, ScrythonRequestHandler):
  _endpoint = '/sets/:id'

class Sets:
  """
  Factory class for accessing Scryfall sets endpoints.

  Examples:
      Get all sets:
          all_sets = scrython.Sets()

      Get specific set:
          set_obj = scrython.Sets(code='m21')
          set_obj = scrython.Sets(id='uuid-here')
          set_obj = scrython.Sets(tcgplayer_id=12345)
  """
  def __new__(self, **kwargs):
    if code := kwargs.get('code', None):
      return SetsByCode(**kwargs)

    if tcgplayer_id := kwargs.get('tcgplayer_id', None):
      return SetsByTCGPlayerId(id=tcgplayer_id, **kwargs)

    if _id := kwargs.get('id', None):
      return SetsById(**kwargs)

    return AllSets(**kwargs)