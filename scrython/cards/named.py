from .cards_object import CardsObject
import urllib.parse

class Named(CardsObject):
	"""
	cards/named
	Gets a card by the name.

	Positional arguments:
		fuzzy : str ................ Uses the fuzzy parameter for the card name.
		or
		exact : str ................ Uses the exact parameter for the card name.

	Optional arguments:
		set : str . Returns the set of the card if specified. Requires the 3 letter set code.
		All arguments are inherited from CardsObject

	Attributes:
		All attributes are inherited from CardsObject

	Example usage:
		>>> card = scrython.cards.Named(exact="Black Lotus")
		>>> card.colors()
	"""
	def __init__(self, **kwargs):
		self.dict = {
			'set':kwargs.get('set', '')
		}

		if kwargs.get('exact') is not None:
			self.dict['exact'] = kwargs.get('exact')

		if kwargs.get('fuzzy') is not None:
			self.dict['fuzzy'] = kwargs.get('fuzzy')

		self.args = urllib.parse.urlencode(self.dict)
		self.url = 'cards/named?' + self.args
		super(Named, self).__init__(self.url)
