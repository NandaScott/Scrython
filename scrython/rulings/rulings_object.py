import asyncio
import aiohttp

class RulingsObject(object):
	def __init__(self, _url, **kwargs):
		self.pretty = kwargs.get('pretty')
		self.format = kwargs.get('format')
		self._url = 'https://api.scryfall.com/' + _url
		loop = asyncio.get_event_loop()
		self.session = aiohttp.ClientSession(loop=loop)

		async def getRequest(url, **kwargs):
			async with self.session.get(url, **kwargs) as response:
				return await response.json()

		self.scryfallJson = loop.run_until_complete(getRequest(
			url = self._url,
			params={
				'format': self.format,
				'pretty': self.pretty
			}))

		if self.scryfallJson['object'] == 'error':
			self.session.close()
			raise Exception(self.scryfallJson['details'])

		self.session.close()

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
			return KeyError('This ruling object has no associated object key.')

		return self.scryfallJson['object']

	def has_more(self):
		if self.__checkForKey('has_more') is None:
			return KeyError('This ruling object has no associated has_more key.')

		return self.scryfallJson['has_more']

	def data(self):
		if self.__checkForKey('data') is None:
			return KeyError('This ruling object has no associated data key.')

		return self.scryfallJson['data']

	def data_length(self):
		if self.__checkForKey('data') is None:
			return KeyError('This ruling object has no associated data key.')

		return len(self.scryfallJson['data'])

	def ruling_object(self, num):
		if self.__checkForTupleKey('data', num, 'object') is None:
			return KeyError('This ruling has no object key.')

		return self.scryfallJson['data'][num]['object']

	def ruling_source(self, num):
		if self.__checkForTupleKey('data', num, 'source') is None:
			return KeyError('This ruling has no source key.')

		return self.scryfallJson['data'][num]['source']

	def ruling_published_at(self, num):
		if self.__checkForTupleKey('data', num, 'published_at') is None:
			return KeyError('This ruling has no published_at key.')

		return self.scryfallJson['data'][num]['published_at']

	def ruling_comment(self, num):
		if self.__checkForTupleKey('data', num, 'comment') is None:
			return KeyError('This ruling has no comment key.')

		return self.scryfallJson['data'][num]['comment']
