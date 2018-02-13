from .cards_object import CardsObject
import urllib.parse

class Mtgo(CardsObject):
	def __init__(self, **kwargs):
		self.mtgoid = kwargs.get('id')
		self.url = 'cards/mtgo/' + str(self.mtgoid)
		super(Mtgo, self).__init__(self.url)
