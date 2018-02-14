from .cards_object import CardsObject

class Collector(CardsObject):
	def __init__(self, **kwargs):
		if kwargs.get('code') is None:
			raise TypeError('No code provided to search by')

		self.url = 'cards/{}/{}?'.format(kwargs.get('code'), str(kwargs.get('collector_number')))
		super(Collector, self).__init__(self.url)
