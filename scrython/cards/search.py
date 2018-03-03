from .cards_object import CardsObject
import urllib.parse

class Search(CardsObject):
	"""
	cards/search
	Uses a search query to gather relevant data.

	Positional arguments:
		q : str ...... The query to search. This will be updated in the future.

	Optional arguments:
		order : str ................... The order you'd like the data returned.
		unique : str ........................... A way to filter similar cards.
		dir : str ......... The direction you'd like to sort. (asc, desc, auto)
		include_extras : bool ... Includes cards that are normally omitted from
								  search results, like Un-sets.
		page : int .............. The page number you'd like to search, if any.
		Inherits all arguments from CardsObject.

	Attributes:
		object : str ....................... Returns what kind of object it is.
		total_cards : int ......... How many cards are returned from the query.
		data : list ...................... The list of potential autocompletes.
		has_more : bool ......... True if there is more than 1 page of results.
		next_page : str ............ The API URI to the next page of the query.

	Example usage:
		>>> search = scrython.cards.Search(q="++e:A25", order="spoiled")
		>>> search.data()
	"""
	def __init__(self, **kwargs):
		if kwargs.get('q') is None:
			raise TypeError('No query is specified.')

		self.dict = {
			'q':kwargs.get('q'),
			'order':kwargs.get('order', 'none'),
			'unique':kwargs.get('unique', 'none'),
			'dir':kwargs.get('dir', 'none'),
			'include_extras':kwargs.get('include_extras', 'false'),
			'page':kwargs.get('page', '1')
			}

		self.args = urllib.parse.urlencode(self.dict)
		self.url = 'cards/search?' + self.args

		super(Search, self).__init__(self.url)

	def object(self):
		super(Search, self)._checkForKey('object')

		return self.scryfallJson['object']

	def total_cards(self):
		super(Search, self)._checkForKey('total_cards')

		return self.scryfallJson['total_cards']

	def data(self):
		super(Search, self)._checkForKey('data')

		return self.scryfallJson['data']

	def next_page(self):
		super(Search, self)._checkForKey('next_page')

		return self.scryfallJson['next_page']

	def warnings(self):
		super(Search, self)._checkForKey('warnings')

		return self.scryfallJson['warnings']

	def data_length(self):
		super(Search, self)._checkForKey('data')

		return len(self.scryfallJson['data'])

	def data_tuple(self, num):
		super(Search, self)._checkForKey('data')

		return self.scryfallJson['data'][num]

	#The following attributes are only to override the inherited class attributes.
	#This class has no matching attributes but we still need the getRequest function from CardsObject

	def id(self):
		raise AttributeError('Search object has no attribute \'id\'')

	def multiverse_ids(self):
		raise AttributeError('Search object has no attribute \'multiverse_ids\'')

	def mtgo_id(self):
		raise AttributeError('Search object has no attribute \'mtgo_id\'')

	def mtgo_foil_id(self):
		raise AttributeError('Search object has no attribute \'mtgo_foil_id\'')

	def name(self):
		raise AttributeError('Search object has no attribute \'name\'')

	def uri(self):
		raise AttributeError('Search object has no attribute \'uri\'')

	def scryfall_uri(self):
		raise AttributeError('Search object has no attribute \'scryfall_uri\'')

	def layout(self):
		raise AttributeError('Search object has no attribute \'layout\'')

	def highres_image(self):
		raise AttributeError('Search object has no attribute \'highres_image\'')

	def image_uris(self):
		raise AttributeError('Search object has no attribute \'image_uris\'')

	def cmc(self):
		raise AttributeError('Search object has no attribute \'cmc\'')

	def type_line(self):
		raise AttributeError('Search object has no attribute \'type_line\'')

	def oracle_text(self):
		raise AttributeError('Search object has no attribute \'oracle_text\'')

	def mana_cost(self):
		raise AttributeError('Search object has no attribute \'mana_cost\'')

	def colors(self):
		raise AttributeError('Search object has no attribute \'colors\'')

	def color_identity(self):
		raise AttributeError('Search object has no attribute \'color_identity\'')

	def legalities(self):
		raise AttributeError('Search object has no attribute \'legalities\'')

	def reserved(self):
		raise AttributeError('Search object has no attribute \'reserved\'')

	def reprint(self):
		raise AttributeError('Search object has no attribute \'reprint\'')

	def set_code(self):
		raise AttributeError('Search object has no attribute \'	def set_code\'')

	def set_name(self):
		raise AttributeError('Search object has no attribute \'	def set_name\'')

	def set_uri(self):
		raise AttributeError('Search object has no attribute \'set_uri\'')

	def set_search_uri(self):
		raise AttributeError('Search object has no attribute \'set_search_uri\'')

	def scryfall_set_uri(self):
		raise AttributeError('Search object has no attribute \'scryfall_set_uri\'')

	def rulings_uri(self):
		raise AttributeError('Search object has no attribute \'rulings_uri\'')

	def prints_search_uri(self):
		raise AttributeError('Search object has no attribute \'prints_search_uri\'')

	def collector_number(self):
		raise AttributeError('Search object has no attribute \'collector_number\'')

	def digital(self):
		raise AttributeError('Search object has no attribute \'digital\'')

	def rarity(self):
		raise AttributeError('Search object has no attribute \'rarity\'')

	def illustration_id(self):
		raise AttributeError('Search object has no attribute \'illustration_id\'')

	def artist(self):
		raise AttributeError('Search object has no attribute \'artist\'')

	def frame(self):
		raise AttributeError('Search object has no attribute \'frame\'')

	def full_art(self):
		raise AttributeError('Search object has no attribute \'full_art\'')

	def border_color(self):
		raise AttributeError('Search object has no attribute \'border_color\'')

	def timeshifted(self):
		raise AttributeError('Search object has no attribute \'timeshifted\'')

	def colorshifted(self):
		raise AttributeError('Search object has no attribute \'colorshifted\'')

	def futureshifted(self):
		raise AttributeError('Search object has no attribute \'futureshifted\'')

	def edhrec_rank(self):
		raise AttributeError('Search object has no attribute \'edhrec_rank\'')

	def currency(self, mode):
		raise AttributeError('Search object has no attribute \'currency(self,\'')

	def related_uris(self):
		raise AttributeError('Search object has no attribute \'related_uris\'')

	def purchase_uris(self):
		raise AttributeError('Search object has no attribute \'purchase_uris\'')

	def life_modifier(self):
		raise AttributeError('Search object has no attribute \'life_modifier\'')

	def hand_modifier(self):
		raise AttributeError('Search object has no attribute \'hand_modifier\'')

	def color_indicator(self):
		raise AttributeError('Search object has no attribute \'color_indicator\'')

	def all_parts(self):
		raise AttributeError('Search object has no attribute \'all_parts\'')

	def card_faces(self):
		raise AttributeError('Search object has no attribute \'card_faces\'')

	def watermark(self):
		raise AttributeError('Search object has no attribute \'watermark\'')

	def story_spotlight_number(self):
		raise AttributeError('Search object has no attribute \'story_spotlight_number\'')

	def story_spotlight_uri(self):
		raise AttributeError('Search object has no attribute \'story_spotlight_uri\'')
