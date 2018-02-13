from .cards_object import CardsObject
import urllib.parse

class Named(CardsObject):
	def __init__(self, **kwargs):
		self.exact = kwargs.get('exact')
		self.fuzzy = kwargs.get('fuzzy')
		self.set = kwargs.get('set', 'None')
		self.dict = {}

		if self.exact is not None:
			self.dict['exact'] = self.exact

		if self.fuzzy is not None:
			self.dict['fuzzy'] = self.fuzzy

		if self.set is not None:
			self.dict['set'] = self.set

		self.args = urllib.parse.urlencode(self.dict)
		self.url = 'cards/named?' + self.args
		super(Named, self).__init__(self.url)
