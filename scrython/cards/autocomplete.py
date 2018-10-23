from .cards_object import CardsObject
import urllib.parse

class Autocomplete(CardsObject):
    """
    cards/autocomplete
    Get a list of potential autocompletion phrases.

    Args:
        q (string):
            The query of the autocompletion.
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

    Example usage:
        >>> auto = scrython.cards.Autocomplete(q="Thal")
        >>> auto.total_items()
    """
    def __init__(self, **kwargs):
        if kwargs.get('q') is None:
            raise TypeError('No query provided to search by')

        self.dict = { 'q': kwargs.get('q') }

        self.args = urllib.parse.urlencode(self.dict)
        self.url = 'cards/autocomplete?' + self.args
        super(Autocomplete, self).__init__(self.url)

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
        super(Autocomplete, self)._checkForKey('object')

        return self.scryfallJson['object']

    def total_values(self):
        """How many items are returned in `data`
        
        Returns:
            int: The number of items in the `data` key
        """
        super(Autocomplete, self)._checkForKey('total_values')

        return self.scryfallJson['total_values']

    def data(self):
        """The list of potential autocompletes
        
        Returns:
            list: A list of possible corrections
        """
        super(Autocomplete, self)._checkForKey('data')

        return self.scryfallJson['data']