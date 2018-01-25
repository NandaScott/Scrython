import aiohttp
import asyncio


class ScryfallObject(object):
	"""docstring for ScryfallObject."""
	def __init__(self, **kwargs):
		self.format = kwargs.get('format')
		self.face = kwargs.get('face')
		self.version = kwargs.get('version')
		self.pretty = kwargs.get('pretty')
		loop = asyncio.get_event_loop()
		self.session = aiohttp.ClientSession(loop=loop)

		async def getRequest(url, **kwargs):
			async with self.session.get(url, **kwargs) as response:
				return await response.json()

	def object(self):
		return self.scryfallJson['object']

	def id(self):
		return self.scryfallJson['id']

	def multiverse_ids(self):
		return self.scryfallJson['multiverse_ids']

	def mtgo_id(self):
		return self.scryfallJson['mtgo_id']

	def mtgo_foil_id(self):
		return self.scryfallJson['mtgo_foil_id']

	def name(self):
		return self.scryfallJson['name']

	def uri(self):
		return self.scryfallJson['uri']

	def scryfall_uri(self):
		return self.scryfallJson['scryfall_uri']

	def layout(self):
		return self.scryfallJson['layout']

	def highres_image(self):
		return self.scryfallJson['highres_image']

	def image_uris(self):
		return self.scryfallJson['image_uris']

	def cmc(self):
		return self.scryfallJson['cmc']

	def type_line(self):
		return self.scryfallJson['type_line']

	def oracle_text(self):
		return self.scryfallJson['oracle_text']

	def mana_cost(self):
		return self.scryfallJson['mana_cost']

	def colors(self):
		return self.scryfallJson['colors']

	def color_identity(self):
		return self.scryfallJson['color_identity']

	def legalities(self):
		return self.scryfallJson['legalities']

	def reserved(self):
		return self.scryfallJson['reserved']

	def reprint(self):
		return self.scryfallJson['reprint']

	def set(self):
		return self.scryfallJson['set']

	def set_name(self):
		return self.scryfallJson['set_name']

	def set_uri(self):
		return self.scryfallJson['set_uri']

	def set_search_uri(self):
		return self.scryfallJson['set_search_uri']

	def scryfall_set_uri(self):
		return self.scryfallJson['scryfall_set_uri']

	def rulings_uri(self):
		return self.scryfallJson['rulings_uri']

	def prints_search_uri(self):
		return self.scryfallJson['prints_search_uri']

	def collector_number(self):
		return self.scryfallJson['collector_number']

	def digital(self):
		return self.scryfallJson['digital']

	def rarity(self):
		return self.scryfallJson['rarity']

	def illustration_id(self):
		return self.scryfallJson['illustration_id']

	def artist(self):
		return self.scryfallJson['artist']

	def frame(self):
		return self.scryfallJson['frame']

	def full_art(self):
		return self.scryfallJson['full_art']

	def border_color(self):
		return self.scryfallJson['border_color']

	def timeshifted(self):
		return self.scryfallJson['timeshifted']

	def colorshifted(self):
		return self.scryfallJson['colorshifted']

	def futureshifted(self):
		return self.scryfallJson['futureshifted']

	def edhrec_rank(self):
		return self.scryfallJson['edhrec_rank']

	def currency(self, mode):
		modes = ['usd', 'eur', 'tix']
		if mode not in modes:
			return KeyError("That currency is not available.")
		return self.scryfallJson[mode]

	def related_uris(self):
		return self.scryfallJson['related_uris']

	def purchase_uris(self):
		return self.scryfallJson['purchase_uris']
