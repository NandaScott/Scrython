import asyncio
import aiohttp
import urllib.parse

class RulingsObject(object):
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
			return KeyError('This object has no key \'object\'')

		return self.scryfallJson['object']

	def has_more(self):
		if self.__checkForKey('has_more') is None:
			return KeyError('This object has no key \'has_more\'')

		return self.scryfallJson['has_more']

	def data(self):
		if self.__checkForKey('data') is None:
			return KeyError('This object has no key \'data\'')

		return self.scryfallJson['data']

	def data_length(self):
		if self.__checkForKey('data') is None:
			return KeyError('This object has no key \'data\'')

		return len(self.scryfallJson['data'])

	def ruling_object(self, num):
		if self.__checkForTupleKey('data', num, 'object') is None:
			return KeyError('This ruling has no key \'object\'')

		return self.scryfallJson['data'][num]['object']

	def ruling_source(self, num):
		if self.__checkForTupleKey('data', num, 'source') is None:
			return KeyError('This ruling has no key \'source\'')

		return self.scryfallJson['data'][num]['source']

	def ruling_published_at(self, num):
		if self.__checkForTupleKey('data', num, 'published_at') is None:
			return KeyError('This ruling has no key \'published_at\'')

		return self.scryfallJson['data'][num]['published_at']

	def ruling_comment(self, num):
		if self.__checkForTupleKey('data', num, 'comment') is None:
			return KeyError('This ruling has no key \'comment\'')

		return self.scryfallJson['data'][num]['comment']
