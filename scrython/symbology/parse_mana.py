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

	#The following attributes are only to override the inherited class attributes.
	#This class has no matching attributes but we still need the getRequest from SymbologyObject

	def appears_in_mana_costs(self):
		raise AttributeError('This object has no attribute \'appears_in_mana_costs\'')

	def funny(self):
		raise AttributeError('This object has no attribute \'funny\'')

	def loose_variant(self):
		raise AttributeError('This object has no attribute \'loose_variant\'')

	def represents_mana(self):
		raise AttributeError('This object has no attribute \'represents_mana\'')

	def symbol(self):
		raise AttributeError('This object has no attribute \'symbol\'')

	def transposable(self):
		raise AttributeError('This object has no attribute \'transposable\'')
