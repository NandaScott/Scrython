from .scryfall_object import ScryfallObject

class Multiverse(ScryfallObject):
	"""
	Parameters:
		id: int		The multiverse id of the card.
	"""

	def __init__(self, **kwargs):
		self.multiverseid = kwargs.get('id')
		self.url = 'cards/multiverse/' + self.multiverseid
		super(Multiverse, self).__init__(self.url)
