from ..base import ScrythonRequestHandler
from ..base_mixins import ScryfallListMixin
from .bulk_data_mixins import BulkDataObjectMixin

class BulkDataObject(BulkDataObjectMixin):
  """
  Wrapper class for individual bulk data objects from Scryfall API responses.

  Provides access to all bulk data properties through BulkDataObjectMixin.
  """
  def __init__(self, data):
    self.scryfall_data = data

class AllBulkData(ScryfallListMixin, ScrythonRequestHandler):
  """
  Get information about all available bulk data files.

  Endpoint: GET /bulk-data

  Returns a list of all Bulk Data objects. Scryfall provides bulk data files
  containing complete datasets of cards, rulings, and other information. These
  files are updated approximately every 12 hours.

  Example:
      # Get all bulk data options
      all_bulk = scrython.bulk_data.AllBulkData()

      # List available files
      for bulk in all_bulk.data:
          print(f"{bulk.name}: {bulk.description}")
          print(f"Size: {bulk.size / 1_000_000:.1f} MB")
          print(f"Download: {bulk.download_uri}")
          print()

  See: https://scryfall.com/docs/api/bulk-data
  """
  _endpoint = '/bulk-data'
  list_data_type = BulkDataObject

class BulkDataById(BulkDataObjectMixin, ScrythonRequestHandler):
  """
  Get information about a specific bulk data file by its Scryfall ID.

  Endpoint: GET /bulk-data/:id

  Returns a single Bulk Data object. Use this to get download URIs and metadata
  for specific bulk data files.

  Args:
      id: The Scryfall UUID for the bulk data file (required).

  Example:
      bulk = scrython.bulk_data.BulkDataById(id='uuid-here')
      print(f"File: {bulk.name}")
      print(f"Last updated: {bulk.updated_at}")
      print(f"Download from: {bulk.download_uri}")

  See: https://scryfall.com/docs/api/bulk-data/id
  """
  _endpoint = '/bulk-data/:id'

class BulkDataByType(BulkDataObjectMixin, ScrythonRequestHandler):
  """
  Get information about a specific bulk data file by its type.

  Endpoint: GET /bulk-data/:type

  Returns a single Bulk Data object for the specified type. This is the most
  convenient way to access standard bulk data files like oracle cards or
  default cards.

  Args:
      type: The bulk data type (required).
          Common types: 'oracle_cards', 'unique_artwork', 'default_cards',
                       'all_cards', 'rulings'

  Example:
      # Get Oracle Cards bulk data
      oracle = scrython.bulk_data.BulkDataByType(type='oracle_cards')
      print(f"Oracle Cards file: {oracle.name}")
      print(f"Size: {oracle.size / 1_000_000:.1f} MB")
      print(f"Updated: {oracle.updated_at}")

      # Download the file
      import requests
      response = requests.get(oracle.download_uri)
      cards = response.json()
      print(f"Downloaded {len(cards)} cards")

  See: https://scryfall.com/docs/api/bulk-data/type
  """
  _endpoint = '/bulk-data/:type'

class BulkData:
  """
  Smart factory for accessing all Scryfall bulk data endpoints.

  This factory routes to the appropriate endpoint class based on the parameters
  provided. Use this instead of importing individual endpoint classes directly
  for a more convenient API. If no parameters are provided, returns information
  about all available bulk data files.

  Bulk data files are large JSON files containing complete datasets of cards and
  other Scryfall information. They're updated approximately every 12 hours and
  are ideal for:
  - Building offline card databases
  - Performing large-scale analysis
  - Avoiding rate limits when processing thousands of cards

  Supported Modes:

      Get all bulk data options (default):
          all_bulk = BulkData()

      Get bulk data by type:
          oracle_cards = BulkData(type='oracle_cards')
          all_cards = BulkData(type='all_cards')
          rulings = BulkData(type='rulings')

      Get bulk data by Scryfall ID:
          bulk = BulkData(id='uuid-here')

  Returns:
      An instance of the appropriate endpoint class (AllBulkData, BulkDataByType, etc.)
      based on the parameters provided. Defaults to AllBulkData if no parameters given.

  Example:
      import scrython
      import requests

      # Get Oracle Cards bulk data
      oracle = scrython.BulkData(type='oracle_cards')
      print(f"Downloading {oracle.size / 1_000_000:.1f} MB...")

      # Download and process
      response = requests.get(oracle.download_uri)
      cards = response.json()

      # Now you have all cards locally - no rate limiting needed!
      for card in cards:
          if 'Lightning' in card['name']:
              print(card['name'])

  Note:
      Files are compressed with gzip and may be several hundred megabytes.
      Card prices become unreliable after 24 hours.

  See: https://scryfall.com/docs/api/bulk-data
  """
  def __new__(self, **kwargs):
    if _id := kwargs.get('id', None):
      return BulkDataById(**kwargs)

    if _type := kwargs.get('type', None):
      return BulkDataByType(**kwargs)

    return AllBulkData(**kwargs)