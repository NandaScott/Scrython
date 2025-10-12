from functools import cache

class ScryfallListMixin:
  list_data_type = None

  @property
  def object(self):
    return 'list'
  
  @property
  @cache
  def data(self):
    if self.list_data_type:
      return list(map(lambda data: self.list_data_type(data), self.scryfall_data['data']))

    return self.scryfall_data['data']

  @property
  def has_more(self):
    return self.scryfall_data['has_more']

  @property
  def next_page(self):
    return self.scryfall_data['next_page']

  @property
  def total_cards(self):
    return self.scryfall_data['total_cards']

  @property
  def warnings(self):
    return self.scryfall_data['warnings']

class ScryfallCatalogMixin:
  @property
  def object(self):
    return 'catalog'

  @property
  def uri(self):
    return self.scryfall_data['uri']

  @property
  def total_values(self):
    return self.scryfall_data['total_values']

  @property
  def data(self):
    return self.scryfall_data['data']
