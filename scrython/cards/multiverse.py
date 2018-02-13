from .cards_object import CardsObject

class Multiverse(CardsObject):
	def __init__(self, **kwargs):
		self.multiverseid = kwargs.get('id')
		self.url = 'cards/multiverse/' + self.multiverseid
		super(Multiverse, self).__init__(self.url)
