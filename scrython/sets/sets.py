from scrython.base import ScrythonRequestHandler
from scrython.base_mixins import ScryfallListMixin
from .sets_mixins import SetsObjectMixin

class SetsObject(SetsObjectMixin):
  """
  Wrapper class for individual set objects from Scryfall API responses.

  Provides access to all set properties through SetsObjectMixin.
  """
  def __init__(self, data):
    self.scryfall_data = data

class AllSets(ScryfallListMixin, ScrythonRequestHandler):
  """
  Get all Magic: The Gathering sets in Scryfall's database.

  Endpoint: GET /sets

  Returns a list of all Set objects. Sets are returned in chronological order
  by default. This includes all official sets, promotional sets, and token sets.

  Example:
      # Get all sets
      all_sets = scrython.sets.AllSets()

      # Iterate through sets
      for set_obj in all_sets.data:
          print(f"{set_obj.name} ({set_obj.code}) - {set_obj.card_count} cards")

      # Check if there are more results
      if all_sets.has_more:
          print("More sets available via pagination")

  See: https://scryfall.com/docs/api/sets/all
  """
  _endpoint = '/sets'
  list_data_type = SetsObject

class SetsByCode(SetsObjectMixin, ScrythonRequestHandler):
  """
  Get a set by its three-to-six-letter set code.

  Endpoint: GET /sets/:code

  Returns a single Set object. Set codes are short, unique identifiers for each
  Magic set (e.g., "znr" for Zendikar Rising, "m21" for Core Set 2021).

  Args:
      code: The three-to-six-letter set code (required).

  Example:
      # Get a specific set by code
      set_obj = scrython.sets.SetsByCode(code='m21')
      print(f"{set_obj.name} released on {set_obj.released_at}")
      print(f"Set type: {set_obj.set_type}")
      print(f"Card count: {set_obj.card_count}")

  See: https://scryfall.com/docs/api/sets/code
  """
  _endpoint = '/sets/:code'

class SetsByTCGPlayerId(SetsObjectMixin, ScrythonRequestHandler):
  """
  Get a set by its TCGPlayer group ID.

  Endpoint: GET /sets/tcgplayer/:id

  Returns a single Set object. TCGPlayer group IDs identify product groups on
  TCGPlayer's marketplace. Useful for marketplace integration and price tracking.

  Args:
      id: The TCGPlayer group ID (required).

  Example:
      set_obj = scrython.sets.SetsByTCGPlayerId(id=12345)
      print(f"Set: {set_obj.name}")
      print(f"TCGPlayer ID: {set_obj.tcgplayer_id}")

  See: https://scryfall.com/docs/api/sets/tcgplayer
  """
  _endpoint = '/sets/tcgplayer/:id'

class SetsById(SetsObjectMixin, ScrythonRequestHandler):
  """
  Get a set by its Scryfall UUID.

  Endpoint: GET /sets/:id

  Returns a single Set object. Scryfall IDs are unique UUIDs that permanently
  identify each set in Scryfall's database. This is the canonical way to
  retrieve sets.

  Args:
      id: The Scryfall UUID for the set (required).

  Example:
      set_obj = scrython.sets.SetsById(id='5f8287b1-5bb6-4e8f-9d78-8f3e3b3e1c6d')
      print(f"{set_obj.name} ({set_obj.code})")

  See: https://scryfall.com/docs/api/sets/id
  """
  _endpoint = '/sets/:id'

class Sets:
  """
  Smart factory for accessing all Scryfall sets endpoints.

  This factory routes to the appropriate endpoint class based on the parameters
  provided. Use this instead of importing individual endpoint classes directly
  for a more convenient API. If no parameters are provided, returns all sets.

  Supported Modes:

      Get all sets (default):
          all_sets = Sets()

      Get set by code:
          set_obj = Sets(code='m21')
          set_obj = Sets(code='znr')

      Get set by TCGPlayer ID:
          set_obj = Sets(tcgplayer_id=12345)

      Get set by Scryfall ID:
          set_obj = Sets(id='uuid-here')

  Returns:
      An instance of the appropriate endpoint class (AllSets, SetsByCode, etc.)
      based on the parameters provided. Defaults to AllSets if no parameters given.

  Example:
      import scrython

      # Get all sets
      all_sets = scrython.Sets()
      for set_obj in all_sets.data:
          print(f"{set_obj.name} - {set_obj.released_at}")

      # Get specific set
      znr = scrython.Sets(code='znr')
      print(f"{znr.name} has {znr.card_count} cards")

  See: https://scryfall.com/docs/api/sets
  """
  def __new__(self, **kwargs):
    if code := kwargs.get('code', None):
      return SetsByCode(**kwargs)

    if tcgplayer_id := kwargs.get('tcgplayer_id', None):
      return SetsByTCGPlayerId(id=tcgplayer_id, **kwargs)

    if _id := kwargs.get('id', None):
      return SetsById(**kwargs)

    return AllSets(**kwargs)