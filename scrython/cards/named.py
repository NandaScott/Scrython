from .cards_object import CardsObject
import urllib.parse

class Named(CardsObject):
	def __init__(self, **kwargs):
		self.dict = {
			'set':kwargs.get('set', '')
		}

		if kwargs.get('exact') is not None:
			self.dict['exact'] = kwargs.get('exact')

		if kwargs.get('fuzzy') is not None:
			self.dict['fuzzy'] = kwargs.get('fuzzy')

		self.args = urllib.parse.urlencode(self.dict)
		self.url = 'cards/named?' + self.args
		super(Named, self).__init__(self.url)
