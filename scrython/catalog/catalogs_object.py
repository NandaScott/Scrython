import asyncio
import aiohttp
import urllib.parse
from threading import Thread

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
		self._url = 'https://api.scryfall.com/{0}&{1}'.format(_url, self.encodedParams)

		async def getRequest(client, url, **kwargs):
			async with client.get(url, **kwargs) as response:
				return await response.json()

		async def main(loop):
			async with aiohttp.ClientSession(loop=loop) as client:
				self.scryfallJson = await getRequest(client, self._url)

		def do_everything():
			loop = asyncio.new_event_loop()
			asyncio.set_event_loop(loop)
			loop.run_until_complete(main(loop))

		t = Thread(target=do_everything)
		t.run()

		if self.scryfallJson['object'] == 'error':
			raise Exception(self.scryfallJson['details'])

	def _checkForKey(self, key):
		try:
			return self.scryfallJson[key]
		except Exception:
			raise KeyError('This card has no key \'{}\''.format(key))

	def object(self):
		self._checkForKey('object')

		return self.scryfallJson['object']

	def uri(self):
		self._checkForKey('uri')

		return self.scryfallJson['uri']

	def total_values(self):
		self._checkForKey('total_values')

		return self.scryfallJson['total_values']

	def data(self):
		self._checkForKey('data')

		return self.scryfallJson['data']
