from .symbology_object import SymbologyObject

class ParseMana(SymbologyObject):
	"""
	symbology/parse-mana

	Positional arguments:
		cost : str ....................... The given mana cost you want. (`RUG`)

	Optional arguments:
		All arguments are inherited from SymbologyObject

	Attributes:
		object : str ...... Returns the type of object it is. (card, error, etc)
		mana_cost : str ............................... The formatted mana cost.
		cmc : float ....................... The converted mana cost of the card.
		colors : list ................... A list of all colors in the mana cost.
		colorless : bool ................... True if the mana cost is colorless.
		monocolored : bool .............. True if the mana cost is mono colored.
		multicolored : bool ...... True if the mana cost is a multicolored cost.

	Example usage:
		>>> mana = scrython.symbology.ParseMana(cost="xcug")
		>>> mana.colors()
	"""
	def __init__(self, cost):
		self.cost = cost
		self.url = 'symbology/parse-mana?cost=' + self.cost
		super(ParseMana, self).__init__(self.url)

	def object(self):
		super(ParseMana, self)._checkForKey('object')

		return self.scryfallJson['object']

	def mana_cost(self):
		super(ParseMana, self)._checkForKey('cost')

		return self.scryfallJson['cost']

	def cmc(self):
		super(ParseMana, self)._checkForKey('cmc')

		return self.scryfallJson['cmc']

	def colors(self):
		super(ParseMana, self)._checkForKey('colors')

		return self.scryfallJson['colors']

	def colorless(self):
		super(ParseMana, self)._checkForKey('colorless')

		return self.scryfallJson['colorless']

	def monocolored(self):
		super(ParseMana, self)._checkForKey('monocolored')

		return self.scryfallJson['monocolored']

	def multicolored(self):
		super(ParseMana, self)._checkForKey('multicolored')

		return self.scryfallJson['multicolored']
