import asyncio
import aiohttp
import urllib.parse

class CatalogsObject(object):
	"""
	Master object for all catalog objects.

	Positional Arguments:
		No arguments are required.

	Optional Arguments:
		format : str ................... The format to return. Defaults to JSON.
		pretty : bool ... Makes the returned JSON prettier. The library may not work properly with this setting.

	Attributes:
		object : str ...... Returns the type of object it is. (card, error, etc)
		uri : str .................. The API URI for the endpoint you've called.
		total_values : int ..................... The number of items in `data()`
		data : list .............. A list of all types returned by the endpoint.
	"""
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
