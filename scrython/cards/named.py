from .cards_object import CardsObject
import urllib.parse

class Named(CardsObject):
	def __init__(self, **kwargs):
		self.dict = {
			'exact':kwargs.get('exact', ''),
			'fuzzy':kwargs.get('fuzzy', ''),
			'set':kwargs.get('set', 'none')
		}

		self.args = urllib.parse.urlencode(self.dict)
		self.url = 'cards/named?' + self.args
		super(Named, self).__init__(self.url)
