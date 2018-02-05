import aiohttp
import asyncio

class ScryfallObject(object):
	def __init__(self, _url, **kwargs):
		self._url = 'https://api.scryfall.com/' + _url
		loop = asyncio.get_event_loop()
		self.session = aiohttp.ClientSession(loop=loop)

		async def getRequest(url, **kwargs):
			async with self.session.get(url, **kwargs) as response:
				return await response.json()

		self.scryfallJson = loop.run_until_complete(getRequest(
			url = self._url,
			params={
				'format': kwargs.get('format'),
				'face': kwargs.get('face'),
				'version': kwargs.get('version'),
				'pretty': kwargs.get('pretty')
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

	def object(self):
		if self.__checkForKey('object') is None:
			return KeyError("This card has no associated object key.")

		return self.scryfallJson['object']

	def id(self):
		if self.__checkForKey('id') is None:
			return KeyError("This card has no associated id key.")

		return self.scryfallJson['id']

	def multiverse_ids(self):
		if self.__checkForKey('multiverse_ids') is None:
			return KeyError("This card has no associated multiverse id key.")

		return self.scryfallJson['multiverse_ids']

	def mtgo_id(self):
		if self.__checkForKey('mtgo_id') is None:
			return KeyError("This card has no associated mtgo id key.")

		return self.scryfallJson['mtgo_id']

	def mtgo_foil_id(self):
		if self.__checkForKey('mtgo_foil_id') is None:
			return KeyError("This card has no associate mtgo foil id key.")

		return self.scryfallJson['mtgo_foil_id']

	def name(self):
		if self.__checkForKey('name') is None:
			return KeyError("This card has no associated name key.")

		return self.scryfallJson['name']

	def uri(self):
		if self.__checkForKey('uri') is None:
			return KeyError("This card has no associated uri key.")

		return self.scryfallJson['uri']

	def scryfall_uri(self):
		if self.__checkForKey('scryfall_uri') is None:
			return KeyError("This card has no associated scryfall uri key.")

		return self.scryfallJson['scryfall_uri']

	def layout(self):
		if self.__checkForKey('layout') is None:
			return KeyError("This card has no associated layout key.")

		return self.scryfallJson['layout']

	def highres_image(self):
		if self.__checkForKey('highres_image') is None:
			return KeyError("This card has no associated highres image key.")

		return self.scryfallJson['highres_image']

	def image_uris(self):
		if self.__checkForKey('image_uris') is None:
			return KeyError("This card has no associated image uris key.")

		return self.scryfallJson['image_uris']

	def cmc(self):
		if self.__checkForKey('cmc') is None:
			return KeyError("This card has no associated cmc key.")

		return self.scryfallJson['cmc']

	def type_line(self):
		if self.__checkForKey('type_line') is None:
			return KeyError("This card has no associated type line key.")

		return self.scryfallJson['type_line']

	def oracle_text(self):
		if self.__checkForKey('oracle_text') is None:
			return KeyError("This card has no associated oracle text key.")

		return self.scryfallJson['oracle_text']

	def mana_cost(self):
		if self.__checkForKey('mana_cost') is None:
			return KeyError("This card has no associated mana cost key.")

		return self.scryfallJson['mana_cost']

	def colors(self):
		if self.__checkForKey('colors') is None:
			return KeyError("This card has no associated colors key.")

		return self.scryfallJson['colors']

	def color_identity(self):
		if self.__checkForKey('color_identity') is None:
			return KeyError("This card has no associated color identity key.")

		return self.scryfallJson['color_identity']

	def legalities(self):
		if self.__checkForKey('legalities') is None:
			return KeyError("This card has no associated legalities key.")

		return self.scryfallJson['legalities']

	def reserved(self):
		if self.__checkForKey('reserved') is None:
			return KeyError("This card has no associated  reserved key key.")

		return self.scryfallJson['reserved']

	def reprint(self):
		if self.__checkForKey('reprint') is None:
			return KeyError("This card has no associated reprint key.")

		return self.scryfallJson['reprint']

	def set(self):
		if self.__checkForKey('set') is None:
			return KeyError("This card has no associated set key.")

		return self.scryfallJson['set']

	def set_name(self):
		if self.__checkForKey('set_name') is None:
			return KeyError("This card has no associated set name key.")

		return self.scryfallJson['set_name']

	def set_uri(self):
		if self.__checkForKey('set_uri') is None:
			return KeyError("This card has no associated set uri key.")

		return self.scryfallJson['set_uri']

	def set_search_uri(self):
		if self.__checkForKey('set_search_uri') is None:
			return KeyError("This card has no associated set search uri key.")

		return self.scryfallJson['set_search_uri']

	def scryfall_set_uri(self):
		if self.__checkForKey('scryfall_set_uri') is None:
			return KeyError("This card has no associated scryfall set uri key.")

		return self.scryfallJson['scryfall_set_uri']

	def rulings_uri(self):
		if self.__checkForKey('rulings_uri') is None:
			return KeyError("This card has no associated rulings uri key.")

		return self.scryfallJson['rulings_uri']

	def prints_search_uri(self):
		if self.__checkForKey('prints_search_uri') is None:
			return KeyError("This card has no associated prints search uri key.")

		return self.scryfallJson['prints_search_uri']

	def collector_number(self):
		if self.__checkForKey('collector_number') is None:
			return KeyError("This card has no associated collector number key.")

		return self.scryfallJson['collector_number']

	def digital(self):
		if self.__checkForKey('digital') is None:
			return KeyError("This card has no associated digital key key.")

		return self.scryfallJson['digital']

	def rarity(self):
		if self.__checkForKey('rarity') is None:
			return KeyError("This card has no associated rarity key.")

		return self.scryfallJson['rarity']

	def illustration_id(self):
		if self.__checkForKey('illustration_id') is None:
			return KeyError("This card has no associated illustration id key.")

		return self.scryfallJson['illustration_id']

	def artist(self):
		if self.__checkForKey('artist') is None:
			return KeyError("This card has no associated artist key.")

		return self.scryfallJson['artist']

	def frame(self):
		if self.__checkForKey('frame') is None:
			return KeyError("This card has no associated frame key.")

		return self.scryfallJson['frame']

	def full_art(self):
		if self.__checkForKey('') is None:
			return KeyError("This card has no associated full art key key.")

		return self.scryfallJson['full_art']

	def border_color(self):
		if self.__checkForKey('border_color') is None:
			return KeyError("This card has no associated border color key.")

		return self.scryfallJson['border_color']

	def timeshifted(self):
		if self.__checkForKey('timeshifted') is None:
			return KeyError("This card has no associated timeshifted key key.")

		return self.scryfallJson['timeshifted']

	def colorshifted(self):
		if self.__checkForKey('colorshifted') is None:
			return KeyError("This card has no associated colorshifted key key.")

		return self.scryfallJson['colorshifted']

	def futureshifted(self):
		if self.__checkForKey('futureshifted') is None:
			return KeyError("This card has no associated futureshifted key key.")

		return self.scryfallJson['futureshifted']

	def edhrec_rank(self):
		if self.__checkForKey('edhrec_rank') is None:
			return KeyError("This card has no associated edhrec rank key.")

		return self.scryfallJson['edhrec_rank']

	def currency(self, mode):
		modes = ['usd', 'eur', 'tix']
		if mode not in modes:
			return KeyError("{} is not a key.".format(mode))

		if self.__checkForKey(mode) is None:
			return KeyError("This card has no associated currency {} key".format(mode))

		return self.scryfallJson[mode]

	def related_uris(self):
		if self.__checkForKey('related_uris') is None:
			return KeyError("This card has no associated related uris key.")

		return self.scryfallJson['related_uris']

	def purchase_uris(self):
		if self.__checkForKey('purchase_uris') is None:
			return KeyError("This card has no associated purchase uris key.")

		return self.scryfallJson['purchase_uris']

	def life_modifier(self):
		if self.__checkForKey('life_modifier') is None:
			return KeyError("This card has no associated life modifier key.")

		return self.scryfallJson['life_modifier']

	def hand_modifier(self):
		if self.__checkForKey('hand_modifier') is None:
			return KeyError("This card has no associated hand modifier key.")

		return self.scryfallJson['hand_modifier']

	def color_indicator(self):
		if self.__checkForKey('color_indicator') is None:
			return KeyError("This card has no associated color indicator key.")

		return self.scryfallJson['color_indicator']

	def all_parts(self):
		if self.__checkForKey('all_parts') is None:
			return KeyError("This card has no associated all parts key.")

		return self.scryfallJson['all_parts']

	def card_faces(self):
		if self.__checkForKey('card_faces') is None:
			return KeyError("This card has no associated card faces key.")

		return self.scryfallJson['card_faces']

	def watermark(self):
		if self.__checkForKey('watermark') is None:
			return KeyError("This card has no associated watermark key.")

		return self.scryfallJson['watermark']

	def story_spotlight_number(self):
		if self.__checkForKey('story_spotlight_number') is None:
			return KeyError("This card has no associated story spotlight number key.")

		return self.scryfallJson['story_spotlight_number']

	def story_spotlight_uri(self):
		if self.__checkForKey('story_spotlight_uri') is None:
			return KeyError("This card has no associated story spotlight uri key.")

		return self.scryfallJson['story_spotlight_uri']
