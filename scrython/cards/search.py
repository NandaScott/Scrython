from .scryfall_object import ScryfallObject
import urllib.parse

class Search(ScryfallObject):
	def __init__(self, **kwargs):
		self.q = kwargs.get('q')
		self.order = kwargs.get('order')
		self.dict = {}

		if self.q is not None:
			self.dict['q'] = self.q

		if self.order is not None:
			self.dict['order'] = self.order

		self.args = urllib.parse.urlencode(self.dict)
		self.url = 'cards/search?' + self.args

		super(Search, self).__init__(self.url)

	def __checkForKey(self, key):
		try:
			return self.scryfallJson[key]
		except KeyError:
			return None

	def object(self):
		if self.__checkForKey('object') is None:
			return KeyError('This card has no associated object key.')

		return self.scryfallJson['object']

	def total_cards(self):
		if self.__checkForKey('total_cards') is None:
			return KeyError('This card has no associated total cards key.')

		return self.scryfallJson['total_cards']

	def data(self):
		if self.__checkForKey('data') is None:
			return KeyError('This card has no associated data key.')

		return self.scryfallJson['data']

	def next_page(self):
		if self.__checkForKey('next_page') is None:
			return KeyError('This card has no associated next page key.')

		return self.scryfallJson['next_page']

	def warnings(self):
		if self.__checkForKey('warnings') is None:
			return KeyError('This card has no associated warnings key.')

		return self.scryfallJson['warnings']
