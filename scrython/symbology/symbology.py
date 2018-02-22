from .symbology_object import SymbologyObject

class Symbology(SymbologyObject):
	"""
	/symbology

	Positional arguments:
		No arguments are required.

	Optional arguments:
		All arguments are inherited from SymbologyObject

	Attributes:
		object : str . Returns the type of object it is. (card, error, etc)
		has_more : bool . True if there are more pages to the object.
		data : list . A list of all data returned.
		data_length : int . The length of the data returned.

		The following require an integer as an arg, which acts as a tuple.
		symbol_symbol(num) : str . The plaintext symbol, usually written with curly braces.
		symbol_loose_variant(num) : str . The alternate version of the symbol, without curly braces.
		symbol_transposable(num): bool . True if it's possibly to write the symbol backwards.
		symbol_represents_mana(num): bool . True if this is a mana symbol.
		symbol_cmc(num): float . The total converted mana cost of the symbol.
		symbol_appears_in_mana_costs(num): bool . True if the symbol appears on the mana cost of any card.
		symbol_funny(num): bool . True if the symbol is featured on any funny cards.
		symbol_colors(num): float . An array of all colors in the given symbol.

	Example usage:
		>>> symbol = scrython.symbology.Symbology()
	"""
	def __init__(self):
		self.url = 'symbology?'
		super(Symbology, self).__init__(self.url)

	def __checkForKey(self, key):
		try:
			return self.scryfallJson[key]
		except KeyError:
			return None

	def __checkForTupleKey(self, parent, num, key):
		try:
			return self.scryfallJson[parent][num][key]
		except KeyError:
			return None

	def object(self):
		if self.__checkForKey('object') is None:
			raise KeyError('This object has no key \'object\'')

		return self.scryfallJson['object']

	def has_more(self):
		if self.__checkForKey('has_more') is None:
			raise KeyError('This object has no key \'has_more\'')

		return self.scryfallJson['has_more']

	def data(self):
		if self.__checkForKey('has_more') is None:
			raise KeyError('This object has no key \'data\'')

		return self.scryfallJson['data']

	def data_length(self):
		if self.__checkForKey('data') is None:
			return KeyError('This object has no key \'data\'')

		return len(self.scryfallJson['data'])

	def symbol_symbol(self, num):
		if self.__checkForTupleKey('data', num, 'symbol') is None:
			raise KeyError('This object has no key \'symbol\'')

		return self.scryfallJson['data'][num]['symbol']

	def symbol_loose_variant(self, num):
		if self.__checkForTupleKey('data', num, 'loose_variant') is None:
			raise KeyError('This object has no key \'loose_variant\'')

		return self.scryfallJson['data'][num]['loose_variant']

	def symbol_transposable(self, num):
		if self.__checkForTupleKey('data', num, 'transposable') is None:
			raise KeyError('This object has no key \'transposable\'')

		return self.scryfallJson['data'][num]['transposable']

	def symbol_represents_mana(self, num):
		if self.__checkForTupleKey('data', num, 'represents_mana') is None:
			raise KeyError('This object has no key \'represents_mana\'')

		return self.scryfallJson['data'][num]['represents_mana']

	def symbol_cmc(self, num):
		if self.__checkForTupleKey('data', num, 'cmc') is None:
			raise KeyError('This object has no key \'cmc\'')

		return self.scryfallJson['data'][num]['cmc']

	def symbol_appears_in_mana_costs(self, num):
		if self.__checkForTupleKey('data', num, 'appears_in_mana_costs') is None:
			raise KeyError('This object has no key \'appears_in_mana_costs\'')

		return self.scryfallJson['data'][num]['appears_in_mana_costs']

	def symbol_funny(self, num):
		if self.__checkForTupleKey('data', num, 'funny') is None:
			raise KeyError('This object has no key \'funny\'')

		return self.scryfallJson['data'][num]['funny']

	def symbol_colors(self, num):
		if self.__checkForTupleKey('data', num, 'colors') is None:
			raise KeyError('This object has no key \'colors\'')

		return self.scryfallJson['data'][num]['colors']
