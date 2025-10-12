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
  def __new__(self, **kwargs):
    if _id := kwargs.get('id', None):
      return BulkDataById(**kwargs)

    if _type := kwargs.get('type', None):
      return BulkDataByType(**kwargs)

    return AllBulkData(**kwargs)