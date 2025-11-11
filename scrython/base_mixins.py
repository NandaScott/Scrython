from functools import cache
from typing import List, Any, Optional, Dict

class ScryfallListMixin:
  list_data_type: Optional[type] = None
  scryfall_data: Dict[str, Any]

  @property
  def object(self) -> str:
    return 'list'

  @property
  @cache
  def data(self) -> List[Any]:
    if self.list_data_type:
      return list(map(lambda data: self.list_data_type(data), self.scryfall_data['data']))

    return self.scryfall_data['data']

  @property
  def has_more(self) -> bool:
    return self.scryfall_data['has_more']

  @property
  def next_page(self) -> Optional[str]:
    return self.scryfall_data.get('next_page')

  @property
  def total_cards(self) -> Optional[int]:
    return self.scryfall_data.get('total_cards')

  @property
  def warnings(self) -> Optional[List[str]]:
    return self.scryfall_data.get('warnings')

class ScryfallCatalogMixin:
  scryfall_data: Dict[str, Any]

  @property
  def object(self) -> str:
    return 'catalog'

  @property
  def uri(self) -> str:
    return self.scryfall_data['uri']

  @property
  def total_values(self) -> int:
    return self.scryfall_data['total_values']

  @property
  def data(self) -> List[str]:
    return self.scryfall_data['data']
