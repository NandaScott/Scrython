from .cards_object import CardsObject

class Id(CardsObject):
	"""
	cards/id
	Get a card by the Scryfall id.

	Positional arguments:
		id : str ....................... The Scryfall Id of the card.

	Optional arguments:
		Inherits all arguments from CardsObject.

	Attributes:
		All attributes are inherited from CardsObject.

	Example usage:
		>>> card = scrython.cards.Id(id="5386a61c-4928-4bd1-babe-5b089ab8b2d9")
		>>> card.name()
	"""
	def __init__(self, **kwargs):
		if kwargs.get('id') is None:
			raise TypeError('No id provided to search by')

		self.url = 'cards/{}?'.format(str(kwargs.get('id')))
		super(Id, self).__init__(self.url)
