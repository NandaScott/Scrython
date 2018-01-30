import aiohttp
import asyncio

class ScryfallObject(object):
	"""
	Parameters:
		format: str				The data format to return: json, text, or image. Defaults to json.
		face: str				If using the image format and this parameter has the value back,
									the back face of the card will be returned.
									Will return a 404 if this card has no back face.
		version: str			The image version to return when using the image
									format: small, normal, large, png, art_crop, or border_crop. Defaults to large.
		pretty: bool			If true, the returned JSON will be prettified. Avoid using for production code.

	Attributes:
		object: str				Returns the type of object it is. (card, error, etc)
		id: str					The scryfall id of the card.
		multiverse_ids: arr		The associated multiverse ids of the card.
		mtgo_id: int			The Magic Online id of the card.
		mtgo_foil_id: int		The Magic Online foil id of the card.
		name: str				The full name of the card. Cards with multiple faces are named with '//' as a seperator.
		uri: str				The Scryfall API uri for the card.
		scryfall_uri: str		The full Scryfall page of the card.
		layout: str				The image layout of the card. (normal, transform, etc)
		highres_image: bool		Returns True if the card has a high res image.
		card_image_uris: dict	All image uris of the card in various qualities.
		cmc: float				A float of the converted mana cost of the card.
		type_line: str			The full type line of the card.
		oracle_text: str		The official oracle text of a card.
		mana_cost: str			The full mana cost using shorthanded mana symbols.
		colors: arr				An array of strings with all colors found in the mana cost.
		color_identity: arr		An array of strings with all colors found on the card itself.
		legalities: dict		A dictionary of all formats and their legality.
		reserved: bool			Returns True if the card is on the reserved list.
		reprint: bool			Returns True if the card has been reprinted before.
		set: str				The 3 letter code for the set of the card.
		set_name: str			The full name for the set of the card.
		set_uri: str			The API uri for the full set list of the card.
		set_search_uri: str		Same output as set_uri.
		scryfall_set_uri: str	The full link to the set on Scryfall.
		rulings_uri: str		The API uri for the rulings of the card.
		prints_search_uri: str	TODO: Figure out what this does.
		collector_number: str	The collector number of the card.
		digital: bool			Returns True if the card is the digital version.
		rarity: str				The rarity of the card.
		illustration_id: str	The related id of the card art.
		artist: str				The artist of the card.
		frame: str				The year of the card frame.
		full_art: bool			Returns True if the card is considered full art.
		border_color: str		The color of the card border.
		timeshifted: bool		Returns True if the card is timeshifted.
		colorshifted: bool		Returns True if the card is colorshifted.
		futureshifted: bool		Returns True if the card is futureshifted.
		edhrec_rank: int		The rank of the card on edhrec.com
		tix: int				The MTGO price of the card
		related_uris: dict		A dictionary of related websites for this card.
		purchase_uris: dict		A dictionary of links to purchase the card.
	"""
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
			return KeyError("This card has no associated object.")

		return self.scryfallJson['object']

	def id(self):
		if self.__checkForKey('id') is None:
			return KeyError("This card has no associated id.")

		return self.scryfallJson['id']

	def multiverse_ids(self):
		if self.__checkForKey('multiverse_ids') is None:
			return KeyError("This card has no associated multiverse id.")

		return self.scryfallJson['multiverse_ids']

	def mtgo_id(self):
		if self.__checkForKey('mtgo_id') is None:
			return KeyError("This card has no associated mtgo id.")

		return self.scryfallJson['mtgo_id']

	def mtgo_foil_id(self):
		if self.__checkForKey('mtgo_foil_id') is None:
			return KeyError("This card has no associate mtgo foil id.")

		return self.scryfallJson['mtgo_foil_id']

	def name(self):
		if self.__checkForKey('name') is None:
			return KeyError("This card has no associated name.")

		return self.scryfallJson['name']

	def uri(self):
		if self.__checkForKey('uri') is None:
			return KeyError("This card has no associated uri.")

		return self.scryfallJson['uri']

	def scryfall_uri(self):
		if self.__checkForKey('scryfall_uri') is None:
			return KeyError("This card has no associated scryfall uri.")

		return self.scryfallJson['scryfall_uri']

	def layout(self):
		if self.__checkForKey('layout') is None:
			return KeyError("This card has no associated layout.")

		return self.scryfallJson['layout']

	def highres_image(self):
		if self.__checkForKey('highres_image') is None:
			return KeyError("This card has no associated highres image.")

		return self.scryfallJson['highres_image']

	def image_uris(self):
		if self.__checkForKey('image_uris') is None:
			return KeyError("This card has no associated image uris.")

		return self.scryfallJson['image_uris']

	def cmc(self):
		if self.__checkForKey('cmc') is None:
			return KeyError("This card has no associated cmc.")

		return self.scryfallJson['cmc']

	def type_line(self):
		if self.__checkForKey('type_line') is None:
			return KeyError("This card has no associated type line.")

		return self.scryfallJson['type_line']

	def oracle_text(self):
		if self.__checkForKey('oracle_text') is None:
			return KeyError("This card has no associated oracle text.")

		return self.scryfallJson['oracle_text']

	def mana_cost(self):
		if self.__checkForKey('mana_cost') is None:
			return KeyError("This card has no associated mana cost.")

		return self.scryfallJson['mana_cost']

	def colors(self):
		if self.__checkForKey('colors') is None:
			return KeyError("This card has no associated colors.")

		return self.scryfallJson['colors']

	def color_identity(self):
		if self.__checkForKey('color_identity') is None:
			return KeyError("This card has no associated color identity.")

		return self.scryfallJson['color_identity']

	def legalities(self):
		if self.__checkForKey('legalities') is None:
			return KeyError("This card has no associated legalities.")

		return self.scryfallJson['legalities']

	#TODO: Format error
	def reserved(self):
		if self.__checkForKey('reserved') is None:
			return KeyError("This card has no associated .")

		return self.scryfallJson['reserved']

	def reprint(self):
		if self.__checkForKey('reprint') is None:
			return KeyError("This card has no associated reprint.")

		return self.scryfallJson['reprint']

	def set(self):
		if self.__checkForKey('set') is None:
			return KeyError("This card has no associated set.")

		return self.scryfallJson['set']

	def set_name(self):
		if self.__checkForKey('set_name') is None:
			return KeyError("This card has no associated set name.")

		return self.scryfallJson['set_name']

	def set_uri(self):
		if self.__checkForKey('set_uri') is None:
			return KeyError("This card has no associated set uri.")

		return self.scryfallJson['set_uri']

	def set_search_uri(self):
		if self.__checkForKey('set_search_uri') is None:
			return KeyError("This card has no associated set search uri.")

		return self.scryfallJson['set_search_uri']

	def scryfall_set_uri(self):
		if self.__checkForKey('scryfall_set_uri') is None:
			return KeyError("This card has no associated scryfall set uri.")

		return self.scryfallJson['scryfall_set_uri']

	def rulings_uri(self):
		if self.__checkForKey('rulings_uri') is None:
			return KeyError("This card has no associated rulings uri.")

		return self.scryfallJson['rulings_uri']

	def prints_search_uri(self):
		if self.__checkForKey('prints_search_uri') is None:
			return KeyError("This card has no associated prints search uri.")

		return self.scryfallJson['prints_search_uri']

	def collector_number(self):
		if self.__checkForKey('collector_number') is None:
			return KeyError("This card has no associated collector number.")

		return self.scryfallJson['collector_number']

	#TODO: Format Error
	def digital(self):
		if self.__checkForKey('digital') is None:
			return KeyError("This card has no associated .")

		return self.scryfallJson['digital']

	def rarity(self):
		if self.__checkForKey('rarity') is None:
			return KeyError("This card has no associated rarity.")

		return self.scryfallJson['rarity']

	def illustration_id(self):
		if self.__checkForKey('illustration_id') is None:
			return KeyError("This card has no associated illustration id.")

		return self.scryfallJson['illustration_id']

	def artist(self):
		if self.__checkForKey('artist') is None:
			return KeyError("This card has no associated artist.")

		return self.scryfallJson['artist']

	def frame(self):
		if self.__checkForKey('frame') is None:
			return KeyError("This card has no associated frame.")

		return self.scryfallJson['frame']

	#TODO: Format error
	def full_art(self):
		if self.__checkForKey('') is None:
			return KeyError("This card has no associated .")

		return self.scryfallJson['full_art']

	def border_color(self):
		if self.__checkForKey('border_color') is None:
			return KeyError("This card has no associated border color.")

		return self.scryfallJson['border_color']

	#TODO: Format Error
	def timeshifted(self):
		if self.__checkForKey('timeshifted') is None:
			return KeyError("This card has no associated .")

		return self.scryfallJson['timeshifted']

	#TODO: Format Error
	def colorshifted(self):
		if self.__checkForKey('colorshifted') is None:
			return KeyError("This card has no associated .")

		return self.scryfallJson['colorshifted']

	#TODO: Format Error
	def futureshifted(self):
		if self.__checkForKey('futureshifted') is None:
			return KeyError("This card has no associated .")

		return self.scryfallJson['futureshifted']

	def edhrec_rank(self):
		if self.__checkForKey('edhrec_rank') is None:
			return KeyError("This card has no associated edhrec rank.")

		return self.scryfallJson['edhrec_rank']

	def currency(self, mode):
		modes = ['usd', 'eur', 'tix']
		if mode not in modes:
			return KeyError("This card has no associated currency {}".format(mode))

		if self.__checkForKey(mode) is None:
			return KeyError("This card has no associated currency {}".format(mode))

		return self.scryfallJson[mode]

	def related_uris(self):
		if self.__checkForKey('related_uris') is None:
			return KeyError("This card has no associated related uris.")

		return self.scryfallJson['related_uris']

	def purchase_uris(self):
		if self.__checkForKey('purchase_uris') is None:
			return KeyError("This card has no associated purchase uris.")

		return self.scryfallJson['purchase_uris']
