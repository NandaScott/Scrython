from .cards_object import CardsObject

class Collector(CardsObject):
	"""
	cards/collector
	Get a card by collector number.

	Positional arguments:
		code : str ....................... This is the 3 letter code for the set
		collector_number : str ........ This is the collector number of the card

	Optional arguments:
		Inherits all arguments from CardsObject

		lang : str ............................... A 2-3 character language code

	Attributes:
		Inherits all attributes from CardsObject

	Example usage:
		>>> card = scrython.cards.Collector(code='exo', collector_number='96')
		>>> card.id()
	"""
	def __init__(self, **kwargs):
		if kwargs.get('code') is None:
			raise TypeError('No code provided to search by')

		self.url = 'cards/{}/{}/{}?'.format(
			kwargs.get('code'),
			str(kwargs.get('collector_number')),
			kwargs.get('lang', 'en')
			)
		super(Collector, self).__init__(self.url)
