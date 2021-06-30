import sys
sys.path.append('..')
from scrython.foundation import FoundationObject

class Code(FoundationObject):
    """
    sets/:code
    Get a set with a 3 letter code.

    Args:
        code (string): 
            The 3 letter code of the set.
        format (string, optional):
            Returns data in the specified method. Defaults to JSON.
        pretty (string, optional):
            Returns a prettier version of the json object. Note that this may break functionality with Scrython.

    Returns:
        N/A

    Raises:
        N/A

    Examples:
        >>> set = scrython.sets.Code(code="por")
        >>> set.name()
    """
    def __init__(self, code):
        self._url = 'sets/{}?'.format(code)
        super(Code, self).__init__(self._url)

    def object(self) -> str:
        """Returns the type of object it is
        (card, error, etc)
        
        Returns:
            string
        """
        super(Code, self)._checkForKey('object')

        return self.scryfallJson['object']

    def code(self) -> str:
        """The three letter set code of the set
        
        Returns:
            string
        """
        super(Code, self)._checkForKey('object')

        return self.scryfallJson['code']

    def mtgo_code(self) -> str:
        """The mtgo equivalent of `code()`
        
        Returns:
            string
        """
        super(Code, self)._checkForKey('mtgo_code')

        return self.scryfallJson['mtgo_code']

    def name(self) -> str:
        """The full name of the set
        
        Returns:
            string
        """
        super(Code, self)._checkForKey('name')

        return self.scryfallJson['name']

    def set_type(self) -> str:
        """The type of the set (expansion, commander, etc)
        
        Returns:
            string
        """
        super(Code, self)._checkForKey('set_type')

        return self.scryfallJson['set_type']

    def released_at(self) -> str:
        """The date the set was launched
        
        Returns:
            string
        """
        super(Code, self)._checkForKey('released_at')

        return self.scryfallJson['released_at']

    def block_code(self) -> str:
        """The the letter code for the block the set was in
        
        Returns:
            string
        """
        super(Code, self)._checkForKey('block_code')

        return self.scryfallJson['block_code']

    def block(self) -> str:
        """The full name of the block a set was in
        
        Returns:
            string
        """
        super(Code, self)._checkForKey('block')

        return self.scryfallJson['block']

    def parent_set_code(self) -> str:
        """The set code for the parent set
        
        Returns:
            string
        """
        super(Code, self)._checkForKey('parent_set_code')

        return self.scryfallJson['parent_set_code']

    def card_count(self) -> int:
        """The number of cards in the set
        
        Returns:
            integer
        """
        super(Code, self)._checkForKey('card_count')

        return self.scryfallJson['card_count']

    def digital(self) -> bool:
        """True if this set is only featured on MTGO
        
        Returns:
            boolean
        """
        super(Code, self)._checkForKey('digital')

        return self.scryfallJson['digital']

    def foil_only(self) -> bool:
        """True if this set only has foils
        
        Returns:
            boolean
        """
        super(Code, self)._checkForKey('foil_only')

        return self.scryfallJson['foil_only']

    def icon_svg_uri(self) -> str:
        """A URI to the SVG of the set symbol
        
        Returns:
            string
        """
        super(Code, self)._checkForKey('icon_svg_uri')

        return self.scryfallJson['icon_svg_uri']

    def search_uri(self) -> str:
        """The scryfall API url for the search
        
        Returns:
            string
        """
        super(Code, self)._checkForKey('search_uri')

        return self.scryfallJson['search_uri']
