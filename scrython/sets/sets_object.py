import asyncio
import aiohttp
import urllib.parse
from threading import Thread

class SetsObject(object):
	"""
	The master class for all sets objects.

	Positional arguments:
		No arguments required.

	Optional arguments:
		format : str ................... The format to return. Defaults to JSON.
		pretty : bool ... Makes the returned JSON prettier. The library may not work properly with this setting.

	Attributes:
		object : str ...... Returns the type of object it is. (card, error, etc)
		code : str ........................ The three letter set code of the set
		mtgo_code : str ........................ The mtgo equivalent of `code()`
		name : str ................................... The full name of the set.
		set_type : str ......... The type of the set (expansion, commander, etc)
		released_at : str ....................... The date the set was launched.
		block_code : str ..... The the letter code for the block the set was in.
		block : str ................... The full name of the block a set was in.
		parent_set_code : str ................. The set code for the parent set.
		card_count : int ......................  The number of cards in the set.
		digital : bool .............. True if this set is only featured on MTGO.
		foil : bool ........................... True if this set only has foils.
		icon_svg_uri : str ................  A URI to the SVG of the set symbol.
		search_uri : str .................. The scryfall API url for the search.
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
			raise KeyError('This object has no key \'{}\''.format(key))

	def object(self):
		self._checkForKey('object')

		return self.scryfallJson['object']

	def code(self):
		self._checkForKey('object')

		return self.scryfallJson['code']

	def mtgo_code(self):
		self._checkForKey('mtgo_code')

		return self.scryfallJson['mtgo_code']

	def name(self):
		self._checkForKey('name')

		return self.scryfallJson['name']

	def set_type(self):
		self._checkForKey('set_type')

		return self.scryfallJson['set_type']

	def released_at(self):
		self._checkForKey('released_at')

		return self.scryfallJson['released_at']

	def block_code(self):
		self._checkForKey('block_code')

		return self.scryfallJson['block_code']

	def block(self):
		self._checkForKey('block')

		return self.scryfallJson['block']

	def parent_set_code(self):
		self._checkForKey('parent_set_code')

		return self.scryfallJson['parent_set_code']

	def card_count(self):
		self._checkForKey('card_count')

		return self.scryfallJson['card_count']

	def digital(self):
		self._checkForKey('digital')

		return self.scryfallJson['digital']

	def foil(self):
		self._checkForKey('foil')

		return self.scryfallJson['foil']

	def icon_svg_uri(self):
		self._checkForKey('icon_svg_uri')

		return self.scryfallJson['icon_svg_uri']

	def search_uri(self):
		self._checkForKey('search_uri')

		return self.scryfallJson['search_uri']
