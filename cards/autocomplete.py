import asyncio, aiohttp

class Autocomplete(object):
	""" cards/autocomplete

	Parameters:
		query: str		The string to autocomplete.
		format: str		The data format to return. Currently only supports JSON.
		pretty: bool	If true, the returned JSON will be prettified. Avoid using for production code.

	Attributes:
		object: str			Returns the type of object it is.
		total_items: int	Returns the number of items in data.
		data: arr			The full autocompleted list.

	"""

	def __init__(self, query, **kwargs):
		self.query = query
		self.pretty = kwargs.get('pretty')
		self.format = kwargs.get('format')
		loop = asyncio.get_event_loop()
		self.session = aiohttp.ClientSession(loop=loop)

		async def getRequest(url, **kwargs):
			async with self.session.get(url, **kwargs) as response:
				return await response.json()

		self.scryfallJson = loop.run_until_complete(getRequest(
			url='https://api.scryfall.com/cards/autocomplete?',
			params={'q':self.query, 'pretty':self.pretty, 'format':self.format}))

		if self.scryfallJson['object'] == 'error':
			self.session.close()
			raise Exception(self.scryfallJson['details'])

		self.session.close()

	def __checkForKey(self, key):
		try:
			return self.scryfallJson[key]
		except KeyError:
			return None

	def object(self):
		if self.__checkForKey('object') is None:
			return KeyError('This card has no associated object key.')

		return self.scryfallJson['object']

	def total_items(self):
		if self.__checkForKey('total_items') is None:
			return KeyError('This card has no associated total items key.')

		return self.scryfallJson['total_items']

	def data(self):
		if self.__checkForKey('data') is None:
			return KeyError('This card has no associated data key.')

		return self.scryfallJson['data']
