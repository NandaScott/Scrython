from .scryfall_object import ScryfallObject
import urllib.parse

class Named(ScryfallObject):
	"""
	Parameters:
		exact: str				The exact card name to search for, case insenstive.
		fuzzy: str				A fuzzy card name to search for.
		set: str				A set code to limit the search to one set.
	"""

	def __init__(self, **kwargs):
		self.exact = kwargs.get('exact')
		self.fuzzy = kwargs.get('fuzzy')
		self.set = kwargs.get('set')
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
