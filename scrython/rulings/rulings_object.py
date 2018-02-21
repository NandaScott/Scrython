import asyncio
import aiohttp
import urllib.parse

class RulingsObject(object):
	"""
	Master class for all rulings objects.

	Positional arguments:
		No arguments required.

	Optional arguments:
		format : str ... Returns data in the specified method. Defaults to JSON.
		face : str ... If you're using the `image` format, this will specify if
						you want the front or back face.
		version : str ... If you're using the `image` format, this will specify if
						you want the small, normal, large, etc version of the image.
		pretty : str ... Returns a prettier version of the json object. Note that
						  this may break functionality with Scrython.

	Attributes:
		object : str ...... Returns the type of object it is. (card, error, etc)
		had_more : bool ... If true, this ruling object has more rules than it currently displays.
		data : list .................................. A list of ruling objects.
		data_length : int ....................... The length of the `data` list.

		The following require an integer as an arg, which acts as a tuple.
		ruling_object : str ............. The type of object for a given ruling.
		ruling_source : str .......................... The source of the ruling.
		ruling_published_at : str ...... The date when the ruling was published.
		ruling_comment : str ............................. The effective ruling.
	"""
	def __init__(self, _url, **kwargs):
		self.params = {
			'format': kwargs.get('format', 'json'), 'face': kwargs.get('face', ''),
			'version': kwargs.get('version', ''), 'pretty': kwargs.get('pretty', '')
		}

		self.encodedParams = urllib.parse.urlencode(self.params)
		self._url = 'https://api.scryfall.com/' + _url + "&" + self.encodedParams #Find a fix for this later

		async def getRequest(client, url, **kwargs):
			async with client.get(url, **kwargs) as response:
				return await response.json()

		async def main(loop):
			async with aiohttp.ClientSession(loop=loop) as client:
				self.scryfallJson = await getRequest(client, self._url)

		loop = asyncio.get_event_loop()
		loop.run_until_complete(main(loop))

		if self.scryfallJson['object'] == 'error':
			raise Exception(self.scryfallJson['details'])

	def __checkForKey(self, key):
		try:
			return self.scryfallJson[key]
		except KeyError:
			return None

	def __checkForTupleKey(self, parent, num, key):
		try:
			return self.scryfallJson[parent][num][key]
		except KeyError:
			return None

	def object(self):
		if self.__checkForKey('object') is None:
			raise KeyError('This object has no key \'object\'')

		return self.scryfallJson['object']

	def has_more(self):
		if self.__checkForKey('has_more') is None:
			raise KeyError('This object has no key \'has_more\'')

		return self.scryfallJson['has_more']

	def data(self):
		if self.__checkForKey('data') is None:
			raise KeyError('This object has no key \'data\'')

		return self.scryfallJson['data']

	def data_length(self):
		if self.__checkForKey('data') is None:
			raise KeyError('This object has no key \'data\'')

		return len(self.scryfallJson['data'])

	def ruling_object(self, num):
		if self.__checkForTupleKey('data', num, 'object') is None:
			raise KeyError('This ruling has no key \'object\'')

		return self.scryfallJson['data'][num]['object']

	def ruling_source(self, num):
		if self.__checkForTupleKey('data', num, 'source') is None:
			raise KeyError('This ruling has no key \'source\'')

		return self.scryfallJson['data'][num]['source']

	def ruling_published_at(self, num):
		if self.__checkForTupleKey('data', num, 'published_at') is None:
			raise KeyError('This ruling has no key \'published_at\'')

		return self.scryfallJson['data'][num]['published_at']

	def ruling_comment(self, num):
		if self.__checkForTupleKey('data', num, 'comment') is None:
			raise KeyError('This ruling has no key \'comment\'')

		return self.scryfallJson['data'][num]['comment']
