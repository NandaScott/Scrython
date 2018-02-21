from .cards_object import CardsObject
import urllib.parse

class Mtgo(CardsObject):
	"""
	cards/mtgo
	Get a card by MTGO id.

	Positional arguments:
		id : str ............................. The required mtgo id of the card.

	Optional arguments:
		All arguments are inherited from CardsObject

	Attributes:
		All attributes are inherited from CardsObject

	Example usage:
		>>> card = scrython.cards.Mtgo(id="48296")
		>>> card.set_name()
	"""
	def __init__(self, **kwargs):
		if kwargs.get('id') is None:
			raise TypeError('No id provided to search by')

		self.url = 'cards/mtgo/{}?'.format(str(kwargs.get('id')))
		super(Mtgo, self).__init__(self.url)
