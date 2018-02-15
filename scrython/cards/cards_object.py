import aiohttp
import asyncio
import urllib.parse

class CardsObject(object):
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

	def object(self):
		if self.__checkForKey('object') is None:
			raise KeyError("This card has no key \'object\'")

		return self.scryfallJson['object']

	def id(self):
		if self.__checkForKey('id') is None:
			raise KeyError("This card has no key \'id\'")

		return self.scryfallJson['id']

	def multiverse_ids(self):
		if self.__checkForKey('multiverse_ids') is None:
			raise KeyError("This card has no key \'multiverse_ids\'")

		return self.scryfallJson['multiverse_ids']

	def mtgo_id(self):
		if self.__checkForKey('mtgo_id') is None:
			raise KeyError("This card has no key \'mtgo_id\'")

		return self.scryfallJson['mtgo_id']

	def mtgo_foil_id(self):
		if self.__checkForKey('mtgo_foil_id') is None:
			raise KeyError("This card has no key \'mtgo_foil_id\'")

		return self.scryfallJson['mtgo_foil_id']

	def name(self):
		if self.__checkForKey('name') is None:
			raise KeyError("This card has no key \'name\'")

		return self.scryfallJson['name']

	def uri(self):
		if self.__checkForKey('uri') is None:
			raise KeyError("This card has no key \'uri\'")

		return self.scryfallJson['uri']

	def scryfall_uri(self):
		if self.__checkForKey('scryfall_uri') is None:
			raise KeyError("This card has no key \'scryfall_uri\'")

		return self.scryfallJson['scryfall_uri']

	def layout(self):
		if self.__checkForKey('layout') is None:
			raise KeyError("This card has no key \'layout\'")

		return self.scryfallJson['layout']

	def highres_image(self):
		if self.__checkForKey('highres_image') is None:
			raise KeyError("This card has no key \'highres_image\'")

		return self.scryfallJson['highres_image']

	def image_uris(self):
		if self.__checkForKey('image_uris') is None:
			raise KeyError("This card has no key \'image_uris\'")

		return self.scryfallJson['image_uris']

	def cmc(self):
		if self.__checkForKey('cmc') is None:
			raise KeyError("This card has no key \'cmc\'")

		return self.scryfallJson['cmc']

	def type_line(self):
		if self.__checkForKey('type_line') is None:
			raise KeyError("This card has no key \'type_line\'")

		return self.scryfallJson['type_line']

	def oracle_text(self):
		if self.__checkForKey('oracle_text') is None:
			raise KeyError("This card has no key \'oracle_text\'")

		return self.scryfallJson['oracle_text']

	def mana_cost(self):
		if self.__checkForKey('mana_cost') is None:
			raise KeyError("This card has no key \'mana_cost\'")

		return self.scryfallJson['mana_cost']

	def colors(self):
		if self.__checkForKey('colors') is None:
			raise KeyError("This card has no key \'colors\'")

		return self.scryfallJson['colors']

	def color_identity(self):
		if self.__checkForKey('color_identity') is None:
			raise KeyError("This card has no key \'color_identity\'")

		return self.scryfallJson['color_identity']

	def legalities(self):
		if self.__checkForKey('legalities') is None:
			raise KeyError("This card has no key \'legalities\'")

		return self.scryfallJson['legalities']

	def reserved(self):
		if self.__checkForKey('reserved') is None:
			raise KeyError("This card has no key \'reserved\'")

		return self.scryfallJson['reserved']

	def reprint(self):
		if self.__checkForKey('reprint') is None:
			raise KeyError("This card has no key \'reprint\'")

		return self.scryfallJson['reprint']

	def set_code(self):
		if self.__checkForKey('set') is None:
			raise KeyError("This card has no key \'set\'")

		return self.scryfallJson['set']

	def set_name(self):
		if self.__checkForKey('set_name') is None:
			raise KeyError("This card has no key \'set_name\'")

		return self.scryfallJson['set_name']

	def set_uri(self):
		if self.__checkForKey('set_uri') is None:
			raise KeyError("This card has no key \'set_uri\'")

		return self.scryfallJson['set_uri']

	def set_search_uri(self):
		if self.__checkForKey('set_search_uri') is None:
			raise KeyError("This card has no key \'set_search_uri\'")

		return self.scryfallJson['set_search_uri']

	def scryfall_set_uri(self):
		if self.__checkForKey('scryfall_set_uri') is None:
			raise KeyError("This card has no key \'scryfall_set_uri\'")

		return self.scryfallJson['scryfall_set_uri']

	def rulings_uri(self):
		if self.__checkForKey('rulings_uri') is None:
			raise KeyError("This card has no key \'rulings_uri\'")

		return self.scryfallJson['rulings_uri']

	def prints_search_uri(self):
		if self.__checkForKey('prints_search_uri') is None:
			raise KeyError("This card has no key \'prints_search_uri\'")

		return self.scryfallJson['prints_search_uri']

	def collector_number(self):
		if self.__checkForKey('collector_number') is None:
			raise KeyError("This card has no key \'collector_number\'")

		return self.scryfallJson['collector_number']

	def digital(self):
		if self.__checkForKey('digital') is None:
			raise KeyError("This card has no key \'digital\'")

		return self.scryfallJson['digital']

	def rarity(self):
		if self.__checkForKey('rarity') is None:
			raise KeyError("This card has no key \'rarity\'")

		return self.scryfallJson['rarity']

	def illustration_id(self):
		if self.__checkForKey('illustration_id') is None:
			raise KeyError("This card has no key \'illustration_id\'")

		return self.scryfallJson['illustration_id']

	def artist(self):
		if self.__checkForKey('artist') is None:
			raise KeyError("This card has no key \'artist\'")

		return self.scryfallJson['artist']

	def frame(self):
		if self.__checkForKey('frame') is None:
			raise KeyError("This card has no key \'frame\'")

		return self.scryfallJson['frame']

	def full_art(self):
		if self.__checkForKey('') is None:
			raise KeyError("This card has no key \'full_art\'")

		return self.scryfallJson['full_art']

	def border_color(self):
		if self.__checkForKey('border_color') is None:
			raise KeyError("This card has no key \'border_color\'")

		return self.scryfallJson['border_color']

	def timeshifted(self):
		if self.__checkForKey('timeshifted') is None:
			raise KeyError("This card has no key \'timeshifted\'")

		return self.scryfallJson['timeshifted']

	def colorshifted(self):
		if self.__checkForKey('colorshifted') is None:
			raise KeyError("This card has no key \'colorshifted\'")

		return self.scryfallJson['colorshifted']

	def futureshifted(self):
		if self.__checkForKey('futureshifted') is None:
			raise KeyError("This card has no key \'futureshifted\'")

		return self.scryfallJson['futureshifted']

	def edhrec_rank(self):
		if self.__checkForKey('edhrec_rank') is None:
			raise KeyError("This card has no key \'edhrec_rank\'")

		return self.scryfallJson['edhrec_rank']

	def currency(self, mode):
		modes = ['usd', 'eur', 'tix']
		if mode not in modes:
			raise KeyError("{} is not a key.".format(mode))

		if self.__checkForKey(mode) is None:
			raise KeyError("This card has no currency key {}".format(mode))

		return self.scryfallJson[mode]

	def related_uris(self):
		if self.__checkForKey('related_uris') is None:
			raise KeyError("This card has no key \'related_uris\'")

		return self.scryfallJson['related_uris']

	def purchase_uris(self):
		if self.__checkForKey('purchase_uris') is None:
			raise KeyError("This card has no key \'purchase_uris\'")

		return self.scryfallJson['purchase_uris']

	def life_modifier(self):
		if self.__checkForKey('life_modifier') is None:
			raise KeyError("This card has no key \'life_modifier\'")

		return self.scryfallJson['life_modifier']

	def hand_modifier(self):
		if self.__checkForKey('hand_modifier') is None:
			raise KeyError("This card has no key \'hand_modifier\'")

		return self.scryfallJson['hand_modifier']

	def color_indicator(self):
		if self.__checkForKey('color_indicator') is None:
			raise KeyError("This card has no key \'color_indicator\'")

		return self.scryfallJson['color_indicator']

	def all_parts(self):
		if self.__checkForKey('all_parts') is None:
			raise KeyError("This card has no key \'all_parts\'")

		return self.scryfallJson['all_parts']

	def card_faces(self):
		if self.__checkForKey('card_faces') is None:
			raise KeyError("This card has no key \'card_faces\'")

		return self.scryfallJson['card_faces']

	def watermark(self):
		if self.__checkForKey('watermark') is None:
			raise KeyError("This card has no key \'watermark\'")

		return self.scryfallJson['watermark']

	def story_spotlight_number(self):
		if self.__checkForKey('story_spotlight_number') is None:
			raise KeyError("This card has no key \'story_spotlight_number\'")

		return self.scryfallJson['story_spotlight_number']

	def story_spotlight_uri(self):
		if self.__checkForKey('story_spotlight_uri') is None:
			raise KeyError("This card has no key \'story_spotlight_uri\'")

		return self.scryfallJson['story_spotlight_uri']
