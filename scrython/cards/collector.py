from .cards_object import CardsObject

class Collector(CardsObject):
	def __init__(self, **kwargs):
		self.code = kwargs.get('code')
		self.collector_number = kwargs.get('collector_number')
		self.url = 'cards/{}/{}'.format(self.code, str(self.collector_number))
		super(Collector, self).__init__(self.url)
