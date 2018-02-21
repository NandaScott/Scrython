from .cards_object import CardsObject

class Multiverse(CardsObject):
	"""
	cards/multiverse
	Get a card by Multiverse id

	Positional arguments:
		id : str ....... This is the associated multiverse id of the given card.

	Optional arguments:
		Inherits all arguments from CardsObject

	Attributes:
		Inherits all attributes from CardsObject

	Example usage:
		>>> card = scrython.cards.Multiverse(id='96865')
		>>> card.name()
	"""
	def __init__(self, **kwargs):
		if kwargs.get('id') is None:
			raise TypeError('No id provided to search by')

		self.url = 'cards/multiverse/{}?'.format(str(kwargs.get('id')))
		super(Multiverse, self).__init__(self.url)
