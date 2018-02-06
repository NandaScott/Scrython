from .scryfall_object import ScryfallObject
import urllib.parse

class Mtgo(ScryfallObject):
	""" cards/mtgo/:id

	Parameters:
		id: int		The mtgo id of the card.

	"""

	def __init__(self, **kwargs):
		self.mtgoid = kwargs.get('id')
		self.url = 'cards/mtgo/' + str(self.mtgoid)
		super(Mtgo, self).__init__(self.url)
