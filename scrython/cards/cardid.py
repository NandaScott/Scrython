from .cards_object import CardsObject

class Id(CardsObject):
	def __init__(self, **kwargs):
		if kwargs.get('id') is None:
			raise TypeError('No id provided to search by')

		self.url = 'cards/{}?'.format(str(kwargs.get('id')))
		super(Id, self).__init__(self.url)
