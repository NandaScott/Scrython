from .symbology_object import SymbologyObject

class ParseMana(SymbologyObject):
	def __init__(self, **kwargs):
		self.cost = kwargs.get('cost')
		self.url = 'symbology/parse-mana?cost=' + self.cost
		super(ParseMana, self).__init__(self.url)

	def __checkForKey(self, key):
		try:
			return self.scryfallJson[key]
		except KeyError:
			return None

	def object(self):
		if self.__checkForKey('object') is None:
			raise KeyError('This object has no key \'object\'')

		return self.scryfallJson['object']

	def mana_cost(self):
		if self.__checkForKey('cost') is None:
			raise KeyError('This object has no key \'cost\'')

		return self.scryfallJson['cost']

	def cmc(self):
		if self.__checkForKey('cmc') is None:
			raise KeyError('This object has no key \'cmc\'')

		return self.scryfallJson['cmc']

	def colors(self):
		if self.__checkForKey('colors') is None:
			raise KeyError('This object has no key \'colors\'')

		return self.scryfallJson['colors']

	def colorless(self):
		if self.__checkForKey('colorless') is None:
			raise KeyError('This object has no key \'colorless\'')

		return self.scryfallJson['colorless']

	def monocolored(self):
		if self.__checkForKey('monocolored') is None:
			raise KeyError('This object has no key \'monocolored\'')

		return self.scryfallJson['monocolored']

	def multicolored(self):
		if self.__checkForKey('multicolored') is None:
			raise KeyError('This object has no key \'multicolored\'')

		return self.scryfallJson['multicolored']
