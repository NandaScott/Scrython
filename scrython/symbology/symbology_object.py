import asyncio
import aiohttp
import urllib.parse
from threading import Thread

class SymbologyObject(object):
	"""
	The master class for all symbology objects.

	Positional arguments:
		No arguments required.

	Optional arguments:
		format : str ................... The format to return. Defaults to JSON.
		pretty : bool ... Makes the returned JSON prettier. The library may not work properly with this setting.

	Attributes:
		No attributes to call.
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
