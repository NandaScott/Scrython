from .scryfall_object import ScryfallObject

class Collector(ScryfallObject):
	""" cards/:code/:collector_number

	Parameters:
		code: str				The 3 or 4 letter set code.
		collector_number: int	The collector number of the card.
	"""

	def __init__(self, **kwargs):
		self.code = kwargs.get('code')
		self.collector_number = kwargs.get('collector_number')
		self.url = 'cards/{}/{}'.format(self.code, str(self.collector_number))
		super(Collector, self).__init__(self.url)
