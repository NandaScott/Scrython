from .cards_object import CardsObject

class Multiverse(CardsObject):
	def __init__(self, **kwargs):
		if kwargs.get('id') is None:
			raise TypeError('No id provided to search by')

		self.url = 'cards/multiverse/{}?'.format(str(kwargs.get('id')))
		super(Multiverse, self).__init__(self.url)
