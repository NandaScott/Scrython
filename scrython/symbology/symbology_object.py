import asyncio
import aiohttp
import urllib.parse

class SymbologyObject(object):
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

	def symbol(self):
		if self.__checkForKey('symbol') is None:
			raise KeyError('This object has no key \'symbol\'')

		return self.scryfallJson['symbol']

	def loose_variant(self):
		if self.__checkForKey('loose_variant') is None:
			raise KeyError('This object has no key \'loose_variant\'')

		return self.scryfallJson['loose_variant']

	def transposable(self):
		if self.__checkForKey('transposable') is None:
			raise KeyError('This object has no key \'transposable\'')

		return self.scryfallJson['transposable']

	def represents_mana(self):
		if self.__checkForKey('represents_mana') is None:
			raise KeyError('This object has no key \'represents_mana\'')

		return self.scryfallJson['represents_mana']

	def cmc(self):
		if self.__checkForKey('cmc') is None:
			raise KeyError('This object has no key \'cmc\'')

		return self.scryfallJson['cmc']

	def appears_in_mana_costs(self):
		if self.__checkForKey('appears_in_mana_costs') is None:
			raise KeyError('This object has no key \'appears_in_mana_costs\'')

		return self.scryfallJson['appears_in_mana_costs']

	def funny(self):
		if self.__checkForKey('funny') is None:
			raise KeyError('This object has no key \'funny\'')

		return self.scryfallJson['funny']

	def colors(self):
		if self.__checkForKey('colors') is None:
			raise KeyError('This object has no key \'colors\'')

		return self.scryfallJson['colors']
