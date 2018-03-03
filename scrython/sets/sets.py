from .sets_object import SetsObject

class Sets(SetsObject):
    """
    /sets
    `Sets()` gets it's own special attributes that don't match with the normal set attributes.

    Positional arguments:
        code : str ............................... The 3 letter code of the set.

    Optional arguments:
        All arguments are inherited from SetsObject

    Attributes:
        object : str ... Returns the type of object it is. (card, error, etc)
        has_more : bool ... True if there are more pages available.
        data : list ... List of all data returned.
        data_length : int ... The length of the data returned.

        The following require an integer as an arg, which acts as a tuple.
        set_object(num) : str .................................. The set object.
        set_code(num) : str .............. The three letter set code of the set.
        set_mtgo_code(num) : str .............. The mtgo equivalent of `code()`.
        set_name(num) : str .......................... The full name of the set.
        set_set_type(num) : str ... The type of the set (expansion, commander, etc)
        set_released_at(num) : str .............. The date the set was launched.
        set_block_code(num) : str ... The the letter code for the block the set was in.
        set_block(num) : str .......... The full name of the block a set was in.
        set_parent_set_code(num) : str ........ The set code for the parent set.
        set_card_count(num) : int .............. The number of cards in the set.
        set_digital(num) : bool ..... True if this set is only featured on MTGO.
        set_foil(num) : bool .................. True if this set only has foils.
        set_icon_svg_uri(num) : str ........ A URI to the SVG of the set symbol.
        set_search_uri(num) : str ......... The scryfall API url for the search.

    Example usage:
        >>> set = scrython.sets.Sets()
        >>> set.name(5)
    """
    def __init__(self):
        self._url = 'sets?'
        super(Sets, self).__init__(self._url)

    def _checkForKey(self, key):
        try:
            return self.scryfallJson[key]
        except Exception:
            raise KeyError('This object has no key \'{}\''.format(key))

    def _checkForTupleKey(self, parent, num, key):
        try:
            return self.scryfallJson[parent][num][key]
        except Exception:
            raise KeyError('This object has no key \'{}\''.format(key))

    def object(self):
        self._checkForKey('object')

        return self.scryfallJson['object']

    def has_more(self):
        self._checkForKey('has_more')

        return self.scryfallJson['has_more']

    def data(self):
        self._checkForKey('data')

        return self.scryfallJson['data']

    def data_length(self):
        self._checkForKey('data')

        return len(self.scryfallJson['data'])

    def set_object(self, num):
        self._checkForTupleKey('data', num, 'object')

        return self.scryfallJson['data'][num]['object']

    def set_code(self, num):
        self._checkForTupleKey('data', num, 'code')

        return self.scryfallJson['data'][num]['code']

    def set_mtgo_code(self, num):
        self._checkForTupleKey('data', num, 'mtgo_code')

        return self.scryfallJson['data'][num]['mtgo_code']

    def set_name(self, num):
        self._checkForTupleKey('data', num, 'name')

        return self.scryfallJson['data'][num]['name']

    def set_set_type(self, num):
        self._checkForTupleKey('data', num, 'set_type')

        return self.scryfallJson['data'][num]['set_type']

    def set_released_at(self, num):
        self._checkForTupleKey('data', num, 'released_at')

        return self.scryfallJson['data'][num]['released_at']

    def set_block_code(self, num):
        self._checkForTupleKey('data', num, 'block_code')

        return self.scryfallJson['data'][num]['block_code']

    def set_block(self, num):
        self._checkForTupleKey('data', num, 'block')

        return self.scryfallJson['data'][num]['block']

    def set_parent_set_code(self, num):
        self._checkForTupleKey('data', num, 'parent_set_code')

        return self.scryfallJson['data'][num]['parent_set_code']

    def set_card_count(self, num):
        self._checkForTupleKey('data', num, 'card_count')

        return self.scryfallJson['data'][num]['card_count']

    def set_digital(self, num):
        self._checkForTupleKey('data', num, 'digital')

        return self.scryfallJson['data'][num]['digital']

    def set_foil(self, num):
        self._checkForTupleKey('data', num, 'foil')

        return self.scryfallJson['data'][num]['foil']

    def set_icon_svg_uri(self, num):
        self._checkForTupleKey('data', num, 'icon_svg_uri')

        return self.scryfallJson['data'][num]['icon_svg_uri']

    def set_search_uri(self, num):
        self._checkForTupleKey('data', num, 'search_uri')

        return self.scryfallJson['data'][num]['search_uri']

	#The following attributes are only to override the inherited class attributes.
	#This class has no matching attributes but we still need the getRequest from SetsObject

    def code(self):
        raise AttributeError('This object has no key \'code\'')

    def mtgo_code(self):
        raise AttributeError('This object has no key \'mtgo_code\'')

    def name(self):
        raise AttributeError('This object has no key \'name\'')

    def set_type(self):
        raise AttributeError('This object has no key \'set_type\'')

    def released_at(self):
        raise AttributeError('This object has no key \'released_at\'')

    def block_code(self):
        raise AttributeError('This object has no key \'block_code\'')

    def block(self):
        raise AttributeError('This object has no key \'block\'')

    def parent_set_code(self):
        raise AttributeError('This object has no key \'parent_set_code\'')

    def card_count(self):
        raise AttributeError('This object has no key \'card_count\'')

    def digital(self):
        raise AttributeError('This object has no key \'digital\'')

    def foil(self):
        raise AttributeError('This object has no key \'foil\'')

    def icon_svg_uri(self):
        raise AttributeError('This object has no key \'icon_svg_uri\'')

    def search_uri(self):
        raise AttributeError('This object has no key \'search_uri\'')
