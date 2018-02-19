import asyncio
import aiohttp
import urllib.parse

class CatalogsObject(object):
	def __init__(self, _url, **kwargs):
		self.params = {'format': kwargs.get('format', 'json'), 'pretty': kwargs.get('pretty', '')}

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

	def object(self):
		if self.__checkForKey('object') is None:
			raise KeyError('This object has no key \'object\'')

		return self.scryfallJson['object']

	def uri(self):
		if self.__checkForKey('uri') is None:
			raise KeyError('This object has no key \'uri\'')

		return self.scryfallJson['uri']

	def total_values(self):
		if self.__checkForKey('total_values') is None:
			raise KeyError('This object has no key \'total_values\'')

		return self.scryfallJson['total_values']

	def data(self):
		if self.__checkForKey('data') is None:
			raise KeyError('This object has no key \'data\'')

		return self.scryfallJson['data']
