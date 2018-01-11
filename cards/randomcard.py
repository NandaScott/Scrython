import asyncio, aiohttp
import json

class RandomCard(object):
	""" cards/random

	Parameters:
		format: str				The data format to return: json, text, or image. Defaults to json.
		face: str				If using the image format and this parameter has the value back,
									the back face of the card will be returned.
									Will return a 404 if this card has no back face.
		version: str			The image version to return when using the image
									format: small, normal, large, png, art_crop, or border_crop. Defaults to large.
		pretty: bool				If true, the returned JSON will be prettified. Avoid using for production code.

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
		card.image_uris: dict	All image uris of the card in various qualities.
		cmc: float				A float of the converted mana cost of the card.
		type_line: str			The full type line of the card.
		oracle_text: str		The official oracle text of a card.
		mana_cost: str			The full mana cost using shorthanded mana symbols.
		colors: arr				An array of strings with all colors found in the mana cost.
		color_identity: arr		An array of strings with all colors found in on the card itself.
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

	def __init__(self, _format=None, face=None, version=None, pretty=None):
		self.format = _format
		self.face = face
		self.version = version
		self.pretty = pretty
		loop = asyncio.get_event_loop()
		self.session = aiohttp.ClientSession(loop=loop)

		async def getRequest(url, **kwargs):
			async with self.session.get(url, **kwargs) as response:
				return await response.json()

		self.scryfallJson = loop.run_until_complete(getRequest(
			url='https://api.scryfall.com/cards/random?',
			params={
				'format':self.format,
				'face':self.face,
				'version':self.version,
				'pretty':self.pretty
			}))

		if self.scryfallJson['object'] == 'error':
			raise Exception(self.scryfallJson['details'])
			self.session.close()

		self.session.close()

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

	def tix(self):
		return self.scryfallJson['tix']

	def related_uris(self):
		return self.scryfallJson['related_uris']

	def purchase_uris(self):
		return self.scryfallJson['purchase_uris']
