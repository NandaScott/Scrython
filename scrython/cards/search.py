from .cards_object import CardsObject
import urllib.parse

class Search(CardsObject):
    """
    cards/search
    Uses a search query to gather relevant data.

    Args:
        q (string):
            The query to search. This will be updated in the future.
        order (string, optional):
            Defaults to 'none'
            The order you'd like the data returned.
        unique (string, optional):
            Defaults to 'none'
            A way to filter similar cards.
        dir (string, optional)
            Defaults to 'none'
            The direction you'd like to sort. (asc, desc, auto)
        include_extras (boolean, optional): 
            Defaults to 'false'
            Includes cards that are normally omitted from search results, like Un-sets.
        include_multilingual (boolean, optional):
            Defaults to 'false'
            Includes cards that are in the language specified. (en, ja, etc).
        page (integer, optional):
            Defaults to '1'
            The page number you'd like to search, if any.
        format (string, optional):
            Defaults to 'json'.
            Returns data in the specified method.
        face (string, optional):
            Defaults to empty string.
            If you're using the `image` format,
            this will specify if you want the front or back face.
        version (string, optional):
            Defaults to empty string.
            If you're using the `image` format, this will specify
            if you want the small, normal, large, etc version of the image.
        pretty (string, optional): 
            Defaults to empty string.
            Returns a prettier version of the json object. 
            Note that this may break functionality with Scrython.

    Raises:
        Exception: If the 'q' parameter is not provided.
        Exception: If the object returned is an error.

    Example usage:
        >>> search = scrython.cards.Search(q="++e:A25", order="spoiled")
        >>> search.data()
    """
    def __init__(self, **kwargs):
        if kwargs.get('q') is None:
            raise Exception('No query is specified.')

        self.dict = {
            'q':kwargs.get('q'),
            'order':kwargs.get('order', 'none'),
            'unique':kwargs.get('unique', 'none'),
            'dir':kwargs.get('dir', 'none'),
            'include_extras':kwargs.get('include_extras', 'false'),
            'include_multilingual':kwargs.get('include_multilingual', 'false'),
            'page':kwargs.get('page', '1')
            }

        self.args = urllib.parse.urlencode(self.dict)
        self.url = 'cards/search?' + self.args

        super(Search, self).__init__(self.url)

        # The following block of methods are not compatible with object returned from
        # the cards/autocomplete endpoint. Doing it this way as to not repeat defining another
        # getRequest function in the __init__. Will be refactored in the future.
        del CardsObject.id
        del CardsObject.multiverse_ids
        del CardsObject.mtgo_id
        del CardsObject.mtgo_foil_id
        del CardsObject.name
        del CardsObject.uri
        del CardsObject.scryfall_uri
        del CardsObject.layout
        del CardsObject.highres_image
        del CardsObject.image_uris
        del CardsObject.cmc
        del CardsObject.type_line
        del CardsObject.oracle_text
        del CardsObject.mana_cost
        del CardsObject.colors
        del CardsObject.color_identity
        del CardsObject.legalities
        del CardsObject.reserved
        del CardsObject.reprint
        del CardsObject.set_code
        del CardsObject.set_name
        del CardsObject.set_uri
        del CardsObject.set_search_uri
        del CardsObject.scryfall_set_uri
        del CardsObject.rulings_uri
        del CardsObject.prints_search_uri
        del CardsObject.collector_number
        del CardsObject.digital
        del CardsObject.rarity
        del CardsObject.illustration_id
        del CardsObject.artist
        del CardsObject.frame
        del CardsObject.full_art
        del CardsObject.border_color
        del CardsObject.timeshifted
        del CardsObject.colorshifted
        del CardsObject.futureshifted
        del CardsObject.edhrec_rank
        del CardsObject.currency
        del CardsObject.related_uris
        del CardsObject.purchase_uris
        del CardsObject.life_modifier
        del CardsObject.hand_modifier
        del CardsObject.color_indicator
        del CardsObject.all_parts
        del CardsObject.card_faces
        del CardsObject.watermark
        del CardsObject.story_spotlight
        del CardsObject.power
        del CardsObject.toughness
        del CardsObject.loyalty
        del CardsObject.flavor_text
        del CardsObject.arena_id
        del CardsObject.lang
        del CardsObject.printed_name
        del CardsObject.printed_type_line
        del CardsObject.printed_text
        del CardsObject.oracle_id
        del CardsObject.foil
        del CardsObject.nonfoil
        del CardsObject.oversized

    def object(self):
        """Returns the type of object it is.
        (card, error, etc)
        
        Returns:
            string: The type of object
        """
        super(Search, self)._checkForKey('object')

        return self.scryfallJson['object']

    def total_cards(self):
        """How many cards are returned from the query
        
        Returns:
            integer: The number of cards returned
        """
        super(Search, self)._checkForKey('total_cards')

        return self.scryfallJson['total_cards']

    def data(self):
        """The data returned from the query
        
        Returns:
            list: A list of card objects
        """
        super(Search, self)._checkForKey('data')

        return self.scryfallJson['data']

    def next_page(self):
        """The API URI to the next page of the query
        
        Returns:
            string: A URI to the next page of the query
        """
        super(Search, self)._checkForKey('next_page')

        return self.scryfallJson['next_page']

    def data_length(self):
        """
        
        Returns:
            integer: The length of data returned
        """
        super(Search, self)._checkForKey('data')

        return len(self.scryfallJson['data'])

    def data_tuple(self, num):
        """Accesses an object at the specified index
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            dict: The card object at the specified index
        """
        super(Search, self)._checkForKey('data')

        return self.scryfallJson['data'][num]

    def has_more(self):
        """Determines if there are more pages of results.
        
        Returns:
            boolean: True if there is more than 1 page of results
        """
        super(Search, self)._checkForKey('has_more')

        return self.scryfallJson['has_more']