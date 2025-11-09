from ..base import ScrythonRequestHandler
from ..base_mixins import ScryfallListMixin
from .bulk_data_mixins import BulkDataObjectMixin

class BulkDataObject(BulkDataObjectMixin):
  def __init__(self, data):
    self.scryfall_data = data

class AllBulkData(ScryfallListMixin, ScrythonRequestHandler):
  _endpoint = '/bulk-data'
  list_data_type = BulkDataObject

class BulkDataById(BulkDataObjectMixin, ScrythonRequestHandler):
  _endpoint = '/bulk-data/:id'

class BulkDataByType(BulkDataObjectMixin, ScrythonRequestHandler):
  _endpoint = '/bulk-data/:type'

class BulkData:
  """
  Factory class for accessing Scryfall bulk data endpoints.

  Examples:
      Get all bulk data info:
          all_bulk = scrython.BulkData()

      Get specific bulk data:
          oracle_cards = scrython.BulkData(type='oracle_cards')
          specific = scrython.BulkData(id='uuid-here')
  """
  def __new__(self, **kwargs):
    if _id := kwargs.get('id', None):
      return BulkDataById(**kwargs)

    if _type := kwargs.get('type', None):
      return BulkDataByType(**kwargs)

    return AllBulkData(**kwargs)