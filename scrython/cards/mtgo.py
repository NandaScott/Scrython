from .cards_object import CardsObject
import urllib.parse

class Mtgo(CardsObject):
	def __init__(self, **kwargs):
		if kwargs.get('id') is None:
			raise TypeError('No id provided to search by')

		self.url = 'cards/mtgo/{}?'.format(str(kwargs.get('id')))
		super(Mtgo, self).__init__(self.url)
