import aiohttp
import asyncio
import urllib.parse
from threading import Thread

class CardsObject(object):
	"""
	Master class that all card objects inherit from.

	Positional arguments:
		No positional arguments are required.

	Optional arguments:
		format : str ... Returns data in the specified method. Defaults to JSON.
		face : str ... If you're using the `image` format, this will specify if
						you want the front or back face.
		version : str ... If you're using the `image` format, this will specify if
						you want the small, normal, large, etc version of the image.
		pretty : str ... Returns a prettier version of the json object. Note that
						  this may break functionality with Scrython.
	Attributes:
		object : str  ..... Returns the type of object it is. (card, error, etc)
		id : str  ................................. The scryfall id of the card.
		multiverse_ids : list  ...... The associated multiverse ids of the card.
		mtgo_id : int  ........................ The Magic Online id of the card.
		mtgo_foil_id : int  .............. The Magic Online foil id of the card.
		name : str  ................................. The full name of the card.
		uri : str  .......................... The Scryfall API uri for the card.
		scryfall_uri : str  ................ The full Scryfall page of the card.
		layout : str  ... The image layout of the card. (normal, transform, etc)
		highres_image : bool  ... Returns True if the card has a high res image.
		image_uris : dict  .... All image uris of the card in various qualities.
		cmc : float  ........... A float of the converted mana cost of the card.
		type_line : str  ....................... The full type line of the card.
		oracle_text : str  ................. The official oracle text of a card.
		mana_cost : str  .... The full mana cost using shorthanded mana symbols.
		colors : list  ... An array of strings with all colors found in the mana cost.
		color_identity : list  ... An array of strings with all colors found on the card itself.
		legalities : dict  ..... A dictionary of all formats and their legality.
		reserved : bool  ..... Returns True if the card is on the reserved list.
		reprint : bool  .... Returns True if the card has been reprinted before.
		set_code : str  ............. The 3 letter code for the set of the card.
		set_name : str  ................. The full name for the set of the card.
		set_uri : str  .......... The API uri for the full set list of the card.
		set_search_uri : str  .......................... Same output as set_uri.
		scryfall_set_uri : str  .......... The full link to the set on Scryfall.
		rulings_uri : str  ............ The API uri for the rulings of the card.
		prints_search_uri : str  ... A link to where you can begin paginating all re/prints for this card on Scryfall’s API.
		collector_number : str  .............. The collector number of the card.
		digital : bool  ....... Returns True if the card is the digital version.
		rarity : str  .................................. The rarity of the card.
		illuStringation_id : str  .............. The related id of the card art.
		artist : str  .................................. The artist of the card.
		frame : str  ............................... The year of the card frame.
		full_art : bool  ...... Returns True if the card is considered full art.
		border_color : str  ...................... The color of the card border.
		timeshifted : bool  ........... Returns True if the card is timeshifted.
		colorshifted : bool  ......... Returns True if the card is colorshifted.
		futureshifted : bool  ....... Returns True if the card is futureshifted.
		edhrec_rank : int  .................. The rank of the card on edhrec.com
		currency("<mode>")` : str  ...  Returns currency from modes `usd`, `eur`, and `tix`.
		related_uris : dict  ... A dictionary of related websites for this card.
		purchase_uris : dict  ...... A dictionary of links to purchase the card.
		life_modifier : str  ... This is the cards life modifier value, assuming it's a Vanguard card.
		hand_modifier : str  ... This cards hand modifier value, assuming it's a Vanguard card.
		color_indicator : list  ... An array of all colors found in this card's color indicator.
		all_parts : list  ... This this card is closely related to other cards, this property will be an array with it.
		card_faces : list  ... If it exists, all parts found on a card's face will be found as an object from this array.
		watermark : str  ......... The associated watermark of the card, if any.
		story_spotlight_number : int  ... This card's story spotlight number, if any.
		story_spotlight_uri : str  ... The URI for the card's story article, if any.
		power : str . The power of the creature, if applicable.
		toughness : str . The toughness of the creature, if applicable.
		flavor_text : str . The flavor text of the card, if any.
	"""
	def __init__(self, _url, **kwargs):

		self.params = {
			'format': kwargs.get('format', 'json'), 'face': kwargs.get('face', ''),
			'version': kwargs.get('version', ''), 'pretty': kwargs.get('pretty', '')
		}

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

	def _checkForTupleKey(self, parent, num, key):
		try:
			return self.scryfallJson[parent][num][key]
		except Exception:
			raise KeyError('This tuple has no key \'{}\''.format(key))

	def object(self):
		self._checkForKey('object')

		return self.scryfallJson['object']

	def id(self):
		self._checkForKey('id')

		return self.scryfallJson['id']

	def multiverse_ids(self):
		self._checkForKey('multiverse_ids')

		return self.scryfallJson['multiverse_ids']

	def mtgo_id(self):
		self._checkForKey('mtgo_id')

		return self.scryfallJson['mtgo_id']

	def mtgo_foil_id(self):
		self._checkForKey('mtgo_foil_id')

		return self.scryfallJson['mtgo_foil_id']

	def name(self):
		self._checkForKey('name')

		return self.scryfallJson['name']

	def uri(self):
		self._checkForKey('uri')

		return self.scryfallJson['uri']

	def scryfall_uri(self):
		self._checkForKey('scryfall_uri')

		return self.scryfallJson['scryfall_uri']

	def layout(self):
		self._checkForKey('layout')

		return self.scryfallJson['layout']

	def highres_image(self):
		self._checkForKey('highres_image')

		return self.scryfallJson['highres_image']

	def image_uris(self):
		self._checkForKey('image_uris')

		return self.scryfallJson['image_uris']

	def cmc(self):
		self._checkForKey('cmc')

		return self.scryfallJson['cmc']

	def type_line(self):
		self._checkForKey('type_line')

		return self.scryfallJson['type_line']

	def oracle_text(self):
		self._checkForKey('oracle_text')

		return self.scryfallJson['oracle_text']

	def mana_cost(self):
		self._checkForKey('mana_cost')

		return self.scryfallJson['mana_cost']

	def colors(self):
		self._checkForKey('colors')

		return self.scryfallJson['colors']

	def color_identity(self):
		self._checkForKey('color_identity')

		return self.scryfallJson['color_identity']

	def legalities(self):
		self._checkForKey('legalities')

		return self.scryfallJson['legalities']

	def reserved(self):
		self._checkForKey('reserved')

		return self.scryfallJson['reserved']

	def reprint(self):
		self._checkForKey('reprint')

		return self.scryfallJson['reprint']

	def set_code(self):
		self._checkForKey('set')

		return self.scryfallJson['set']

	def set_name(self):
		self._checkForKey('set_name')

		return self.scryfallJson['set_name']

	def set_uri(self):
		self._checkForKey('set_uri')

		return self.scryfallJson['set_uri']

	def set_search_uri(self):
		self._checkForKey('set_search_uri')

		return self.scryfallJson['set_search_uri']

	def scryfall_set_uri(self):
		self._checkForKey('scryfall_set_uri')

		return self.scryfallJson['scryfall_set_uri']

	def rulings_uri(self):
		self._checkForKey('rulings_uri')

		return self.scryfallJson['rulings_uri']

	def prints_search_uri(self):
		self._checkForKey('prints_search_uri')

		return self.scryfallJson['prints_search_uri']

	def collector_number(self):
		self._checkForKey('collector_number')

		return self.scryfallJson['collector_number']

	def digital(self):
		self._checkForKey('digital')

		return self.scryfallJson['digital']

	def rarity(self):
		self._checkForKey('rarity')

		return self.scryfallJson['rarity']

	def illustration_id(self):
		self._checkForKey('illustration_id')

		return self.scryfallJson['illustration_id']

	def artist(self):
		self._checkForKey('artist')

		return self.scryfallJson['artist']

	def frame(self):
		self._checkForKey('frame')

		return self.scryfallJson['frame']

	def full_art(self):
		self._checkForKey('')

		return self.scryfallJson['full_art']

	def border_color(self):
		self._checkForKey('border_color')

		return self.scryfallJson['border_color']

	def timeshifted(self):
		self._checkForKey('timeshifted')

		return self.scryfallJson['timeshifted']

	def colorshifted(self):
		self._checkForKey('colorshifted')

		return self.scryfallJson['colorshifted']

	def futureshifted(self):
		self._checkForKey('futureshifted')

		return self.scryfallJson['futureshifted']

	def edhrec_rank(self):
		self._checkForKey('edhrec_rank')

		return self.scryfallJson['edhrec_rank']

	def currency(self, mode):
		modes = ['usd', 'eur', 'tix']
		if mode not in modes:
			raise KeyError("{} is not a key.".format(mode))

		self._checkForKey(mode)

		return self.scryfallJson[mode]

	def related_uris(self):
		self._checkForKey('related_uris')

		return self.scryfallJson['related_uris']

	def purchase_uris(self):
		self._checkForKey('purchase_uris')

		return self.scryfallJson['purchase_uris']

	def life_modifier(self):
		self._checkForKey('life_modifier')

		return self.scryfallJson['life_modifier']

	def hand_modifier(self):
		self._checkForKey('hand_modifier')

		return self.scryfallJson['hand_modifier']

	def color_indicator(self):
		self._checkForKey('color_indicator')

		return self.scryfallJson['color_indicator']

	def all_parts(self):
		self._checkForKey('all_parts')

		return self.scryfallJson['all_parts']

	def card_faces(self):
		self._checkForKey('card_faces')

		return self.scryfallJson['card_faces']

	def watermark(self):
		self._checkForKey('watermark')

		return self.scryfallJson['watermark']

	def story_spotlight_number(self):
		self._checkForKey('story_spotlight_number')

		return self.scryfallJson['story_spotlight_number']

	def story_spotlight_uri(self):
		self._checkForKey('story_spotlight_uri')

		return self.scryfallJson['story_spotlight_uri']

	def power(self):
		self._checkForKey('power')

		return self.scryfallJson['power']

	def toughness(self):
		self._checkForKey('toughness')

		return self.scryfallJson['toughness']

	def loyalty(self):
		self._checkForKey('loyalty')

		return self.scryfallJson['loyalty']

	def flavor_text(self):
		self._checkForKey('flavor_text')

		return self.scryfallJson['flavor_text']
