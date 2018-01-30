from .scryfall_object import ScryfallObject

class Id(ScryfallObject):
	""" cards/:id

	Parameters:
		id: str					The Scryfall id of the card.
	"""

	def __init__(self, **kwargs):
		self.id = kwargs.get('id')
		self.url = 'cards/' + str(self.id)
		super(Id, self).__init__(self.url)
