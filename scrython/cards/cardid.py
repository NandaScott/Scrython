from .cards_object import CardsObject

class Id(CardsObject):
	def __init__(self, **kwargs):
		self.id = kwargs.get('id')
		self.url = 'cards/' + str(self.id)
		super(Id, self).__init__(self.url)
