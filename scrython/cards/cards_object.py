import sys
sys.path.append('..')
from scrython.foundation import FoundationObject
import aiohttp
import asyncio
import urllib.parse
from threading import Thread

class CardsObject(FoundationObject):
    """
    Master class that all card objects inherit from.

    Args:
        format (string, optional):
            Defaults to 'json'.
            Returns data in the specified method.
        face (string, optional):
            Defaults to empty string.
            If you're using the `image` format, this will specify if you want the front or back face.
        version (string, optional):
            Defaults to empty string.
            If you're using the `image` format, this will specify if you want the small, normal,
            large, etc version of the image.
        pretty (string, optional):
            Defaults to empty string.
            Returns a prettier version of the json object.
            Note that this may break functionality with Scrython.

    Raises:
        Exception: If the object returned is an error.
    """

    def object(self):
        """Returns the type of object it is
        (card, error, etc)
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('object')

        return self.scryfallJson['object']

    def id(self):
        """A unique ID for the returned card object
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('id')

        return self.scryfallJson['id']

    def multiverse_ids(self):
        """The official Gatherer multiverse ids of the card
        
        Returns:
            list
        """
        super(CardsObject, self)._checkForKey('multiverse_ids')

        return self.scryfallJson['multiverse_ids']

    def mtgo_id(self):
        """The official MTGO id of the of the card
        
        Returns:
            integer: The Magic Online id of the card
        """
        super(CardsObject, self)._checkForKey('mtgo_id')

        return self.scryfallJson['mtgo_id']

    def mtgo_foil_id(self):
        """The corresponding MTGO foil ID of the card
        
        Returns:
            integer: The Magic Online foil id of the card
        """
        super(CardsObject, self)._checkForKey('mtgo_foil_id')

        return self.scryfallJson['mtgo_foil_id']

    def tcgplayer_id(self):
        """The `productId` of the card on TCGplayer.

        Returns:
            integer: The TCGplayer id of the card
        """
        super(CardsObject, self)._checkForKey('tcgplayer_id')

        return self.scryfallJson['tcgplayer_id']

    def tcgplayer_etched_id(self):
        """The `etched_id` of the card on TCGplayer.

        Returns:
            integer: The TCGplayer etched id of the card
        """
        super(CardsObject, self)._checkForKey('tcgplayer_etched_id')

        return self.scryfallJson['tcgplayer_etched_id']

    def name(self):
        """The oracle name of the card
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('name')

        return self.scryfallJson['name']

    def uri(self):
        """The Scryfall API uri for the card
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('uri')

        return self.scryfallJson['uri']

    def scryfall_uri(self):
        """The full Scryfall page of the card
        As if it was a URL from the site.
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('scryfall_uri')

        return self.scryfallJson['scryfall_uri']

    def layout(self):
        """The image layout of the card. (normal, transform, etc)
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('layout')

        return self.scryfallJson['layout']

    def highres_image(self):
        """Determine if a card has a highres scan available
        
        Returns:
            boolean
        """
        super(CardsObject, self)._checkForKey('highres_image')

        return self.scryfallJson['highres_image']

    def image_uris(self, index=0, image_type=None):
        """All image uris of the card in various qualities

        An index and an image type must be supplied a single uri.

        If the card has additional faces, the returned dict will
        default to the front of the card.

        Returns:
            dict: If given no arguments
            string: If given an index and image_type

        Raises:
            Exception: If given no index
            KeyError: If the given image type is not a known type
        """

        layouts = {
            'normal': lambda num: self.scryfallJson['image_uris'],
            'split': lambda num: self.scryfallJson['image_uris'],
            'flip': lambda num: self.scryfallJson['image_uris'],
            'transform': lambda num: self.scryfallJson['card_faces'][num]['image_uris'],
            'meld': lambda num: self.scryfallJson['image_uris'],
            'leveler': lambda num: self.scryfallJson['image_uris'],
            'saga': lambda num: self.scryfallJson['image_uris'],
            'class': lambda num: self.scryfallJson['image_uris'],
            'planar': lambda num: self.scryfallJson['image_uris'],
            'scheme': lambda num: self.scryfallJson['image_uris'],
            'vanguard': lambda num: self.scryfallJson['image_uris'],
            'token': lambda num: self.scryfallJson['image_uris'],
            'double_faced_token': lambda num: self.scryfallJson['card_faces'][num]['image_uris'],
            'emblem': lambda num: self.scryfallJson['image_uris'],
            'augment': lambda num: self.scryfallJson['image_uris'],
            'host': lambda num: self.scryfallJson['image_uris'],
            'adventure': lambda num: self.scryfallJson['image_uris'],
            'modal_dfc': lambda num: self.scryfallJson['card_faces'][num]['image_uris']
        }

        image_types = {
            'small': lambda d: d['small'],
            'normal': lambda d: d['normal'],
            'large': lambda d: d['large'],
            'png': lambda d: d['png'],
            'art_crop': lambda d: d['art_crop'],
            'border_crop': lambda d: d['border_crop']
        }

        images_dict = layouts.get(self.scryfallJson['layout'])

        uri = image_types.get(image_type)

        if index == 0 and image_type is None:
            return images_dict(0)
        elif not isinstance(index, int):
            raise Exception('You must supply an index to get a uri')
        elif image_type not in list(image_types.keys()):
            raise KeyError('Image type not in known types')

        return uri(images_dict(index))

    def cmc(self):
        """A float of the converted mana cost of the card
        
        Returns:
            float: The cmc of the card
        """
        super(CardsObject, self)._checkForKey('cmc')

        return self.scryfallJson['cmc']

    def type_line(self):
        """The full type line of the card
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('type_line')

        return self.scryfallJson['type_line']

    def oracle_text(self):
        """The official oracle text of a card
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('oracle_text')

        return self.scryfallJson['oracle_text']

    def mana_cost(self):
        """The full mana cost using shorthanded mana symbols
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('mana_cost')

        return self.scryfallJson['mana_cost']

    def colors(self):
        """A list of strings with all colors found in the mana cost
        
        Returns:
            list
        """
        super(CardsObject, self)._checkForKey('colors')

        return self.scryfallJson['colors']

    def color_identity(self):
        """A list of strings with all colors found on the card itself
        
        Returns:
            list
        """
        super(CardsObject, self)._checkForKey('color_identity')

        return self.scryfallJson['color_identity']

    def legalities(self):
        """A dictionary of all formats and their legality
        
        Returns:
            dict
        """
        super(CardsObject, self)._checkForKey('legalities')

        return self.scryfallJson['legalities']

    def reserved(self):
        """Returns True if the card is on the reserved list
        
        Returns:
            boolean
        """
        super(CardsObject, self)._checkForKey('reserved')

        return self.scryfallJson['reserved']

    def reprint(self):
        """Returns True if the card has been reprinted before
        
        Returns:
            boolean
        """
        super(CardsObject, self)._checkForKey('reprint')

        return self.scryfallJson['reprint']

    def set_code(self):
        """The 3 letter code for the set of the card
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('set')

        return self.scryfallJson['set']

    def set_name(self):
        """The full name for the set of the card
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('set_name')

        return self.scryfallJson['set_name']

    def set_uri(self):
        """The API uri for the full set list of the card
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('set_uri')

        return self.scryfallJson['set_uri']

    def set_search_uri(self):
        """Same output as set_uri
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('set_search_uri')

        return self.scryfallJson['set_search_uri']

    def scryfall_set_uri(self):
        """The full link to the set on Scryfall
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('scryfall_set_uri')

        return self.scryfallJson['scryfall_set_uri']

    def rulings_uri(self):
        """The API uri for the rulings of the card
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('rulings_uri')

        return self.scryfallJson['rulings_uri']

    def prints_search_uri(self):
        """A link to where you can begin paginating all re/prints for this card on Scryfall’s API
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('prints_search_uri')

        return self.scryfallJson['prints_search_uri']

    def collector_number(self):
        """The collector number of the card
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('collector_number')

        return self.scryfallJson['collector_number']

    def digital(self):
        """Returns True if the card is the digital version
        
        Returns:
            boolean
        """
        super(CardsObject, self)._checkForKey('digital')

        return self.scryfallJson['digital']

    def rarity(self):
        """The rarity of the card
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('rarity')

        return self.scryfallJson['rarity']

    def illustration_id(self):
        """The related id of the card art
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('illustration_id')

        return self.scryfallJson['illustration_id']

    def artist(self):
        """The artist of the card
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('artist')

        return self.scryfallJson['artist']

    def frame(self):
        """The year of the card frame
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('frame')

        return self.scryfallJson['frame']

    def frame_effects(self):
        """The card's frame effect, if any. (miracle, nyxtouched, etc.)
        
        Returns:
            list: The card's frame effects.
        """
        super(CardsObject, self)._checkForKey('frame_effects')

        return self.scryfallJson['frame_effects']

    def full_art(self):
        """Returns True if the card is considered full art
        
        Returns:
            boolean
        """
        super(CardsObject, self)._checkForKey('full_art')

        return self.scryfallJson['full_art']

    def border_color(self):
        """The color of the card border
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('border_color')

        return self.scryfallJson['border_color']

    def edhrec_rank(self):
        """The rank of the card on edhrec.com
        
        Returns:
            int: The rank of the card on edhrec.co
        """
        super(CardsObject, self)._checkForKey('edhrec_rank')

        return self.scryfallJson['edhrec_rank']

    def prices(self, mode):
        """Returns prices from modes `usd`, `usd_foil`, `usd_etched`, `usd_glossy`, `eur`, and `tix`
        
        Args:
            mode (string): The prices to get
        
        Raises:
            KeyError: If the mode parameter does not match a known key
        
        Returns:
            float: The prices as a float
        """
        modes = ['usd', 'usd_foil', 'usd_etched', 'usd_glossy', 'eur', 'tix']
        if mode not in modes:
            raise KeyError("{} is not a key.".format(mode))

        super(CardsObject, self)._checkForKey('prices', mode)

        return self.scryfallJson['prices'][mode]

    def related_uris(self):
        """A dictionary of related websites for this card
        
        Returns:
            dict
        """
        super(CardsObject, self)._checkForKey('related_uris')

        return self.scryfallJson['related_uris']

    def purchase_uris(self):
        """A dictionary of links to purchase the card
        
        Returns:
            dict
        """
        super(CardsObject, self)._checkForKey('purchase_uris')

        return self.scryfallJson['purchase_uris']

    def life_modifier(self):
        """This is the cards life modifier value, assuming it's a Vanguard card
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('life_modifier')

        return self.scryfallJson['life_modifier']

    def hand_modifier(self):
        """This cards hand modifier value, assuming it's a Vanguard card
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('hand_modifier')

        return self.scryfallJson['hand_modifier']

    def color_indicator(self, num):
        """An list of all colors found in this card's color indicator
        
        Returns:
            list
        """
        self._checkForTupleKey('card_faces', num, 'color_indicator')

        return self.scryfallJson['card_faces'][num]['color_indicator']

    def all_parts(self):
        """This this card is closely related to other cards, this property will be an list with it
        
        Returns:
            list
        """
        super(CardsObject, self)._checkForKey('all_parts')

        return self.scryfallJson['all_parts']

    def card_faces(self):
        """If it exists, all parts found on a card's face will be found as an object from this list
        
        Returns:
            list
        """
        super(CardsObject, self)._checkForKey('card_faces')

        return self.scryfallJson['card_faces']

    def watermark(self):
        """The associated watermark of the card, if any
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('watermark')

        return self.scryfallJson['watermark']

    def story_spotlight(self):
        """True if this card is featured in the story
        
        Returns:
            boolean
        """
        super(CardsObject, self)._checkForKey('story_spotlight')

        return self.scryfallJson['story_spotlight']

    def power(self):
        """The power of the creature, if applicable
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('power')

        return self.scryfallJson['power']

    def toughness(self):
        """The toughness of the creature, if applicable
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('toughness')

        return self.scryfallJson['toughness']

    def loyalty(self):
        """This card's loyalty. Some loyalties may be X rather than a number
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('loyalty')

        return self.scryfallJson['loyalty']

    def flavor_text(self):
        """The flavor text of the card, if any
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('flavor_text')

        return self.scryfallJson['flavor_text']

    def arena_id(self):
        """The Arena ID of the card, if any
        
        Returns:
            int: The Arena ID of the card, if any
        """
        super(CardsObject, self)._checkForKey('arena_id')

        return self.scryfallJson['arena_id']

    def lang(self):
        """The language of the card
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('lang')

        return self.scryfallJson['lang']

    def printed_name(self):
        """If the card is in a non-English language, this will be the name as it appears on the card
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('printed_name')

        return self.scryfallJson['printed_name']

    def printed_type_line(self):
        """If the card is in a non-English language, this will be the type line as it appears on the card
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('printed_type_line')

        return self.scryfallJson['printed_type_line']

    def printed_text(self):
        """If the card is in a non-English language, this will be the rules text as it appears on the card
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('printed_text')

        return self.scryfallJson['printed_text']

    def oracle_id(self):
        """A unique ID for this card's oracle text
        
        Returns:
            string
        """
        super(CardsObject, self)._checkForKey('oracle_id')

        return self.scryfallJson['oracle_id']

    def foil(self):
        """True if this printing exists in a foil version.

        DEPRECATION NOTICE: This method will be deprecated on Nov 1, 2021.

        Returns:
            boolean
        """
        super(CardsObject, self)._checkForKey('foil')

        print('WARNING: This method will be deprecated on Nov 1, 2021. Please use the `finishes` method instead.')

        return self.scryfallJson['foil']

    def nonfoil(self):
        """True if this printing does not exist in foil

        DEPRECATION NOTICE: This method will be deprecated on Nov 1, 2021.
        
        Returns:
            boolean
        """
        super(CardsObject, self)._checkForKey('nonfoil')

        print('WARNING: This method will be deprecated on Nov 1, 2021. Please use the `finishes` method instead.')

        return self.scryfallJson['nonfoil']

    def oversized(self):
        """True if this printing is an oversized card
        
        Returns:
            boolean
        """
        super(CardsObject, self)._checkForKey('oversized')

        return self.scryfallJson['oversized']

    def games(self):
        """A list of games that this card print is available in.

        Returns:
            array: A list of games
        """
        super(CardsObject, self)._checkForKey('games')

        return self.scryfallJson['games']

    def promo(self):
        """True if this card is a promotional print.

        Returns:
            boolean
        """
        super(CardsObject, self)._checkForKey('promo')

        return self.scryfallJson['promo']

    def released_at(self):
        """The date this card was first released.
        
        Returns:
            string: The date in ISO format
        """
        super(CardsObject, self)._checkForKey('released_at')

        return self.scryfallJson['released_at']

    def preview(self, key=None):
        """Preview information for this card, if any.
        You may pass the name of a valid key to return the value of that key.
        Such as a source_uri.
        
        Args:
            key (string): A key for specific information about the preview.

        Returns:
            dict: If provided no key, the entire dict is returned.
            string: If provided a key, the value of that key is returned.
        """
        super(CardsObject, self)._checkForKey('preview')

        if key in self.scryfallJson['preview']:
            return self.scryfallJson['preview'][key]

        return self.scryfallJson['preview']

    def image_status(self):
        """Provides insight to the status of the images of the card.

        Returns:
            string: An enum of 'missing', 'placeholder', 'lowres', 'highres_scan'
        """
        super(CardsObject, self)._checkForKey('image_status')

        return self.scryfallJson['image_status']

    def finishes(self):
        """A list of computer-readable flags that indicate if this card
        can come in foil, nonfoil, etched, or glossy finishes.

        Returns:
            list: A list of all finishes.
        """
        super(CardsObject, self)._checkForKey('finishes')

        return self.scryfallJson['finishes']