import asyncio, aiohttp
import json

class CardsAutocomplete(object):
	""" cards/autocomplete

	Parameters:
		format: str		The data format to return. Currently only supports JSON.
		pretty: bool	If true, the returned JSON will be prettified. Avoid using for production code.

	Attributes:
		object: str			Returns the type of object it is.
		total_items: int	Returns the number of items in data.
		data: arr			The full autocompleted list.

	"""

	def __init__(self, query, pretty=None, _format=None):
		self.query = query
		self.pretty = pretty
		self.format = _format
		loop = asyncio.get_event_loop()
		self.session = aiohttp.ClientSession(loop=loop)

		async def getRequest(url, **kwargs):
			async with self.session.get(url, **kwargs) as response:
				return await response.json()

		self.scryfallJson = loop.run_until_complete(getRequest(
			url='https://api.scryfall.com/cards/autocomplete?',
			params={'q':self.query, 'pretty':self.pretty, 'format':self.format}))

		self.session.close()

	def object(self):
		return self.scryfallJson['object']

	def total_items(self):
		return self.scryfallJson['total_items']

	def data(self):
		return self.scryfallJson['data']
