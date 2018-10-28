import sys
sys.path.append('..')
from scrython.foundation import FoundationObject

class Sets(FoundationObject):
    """
    /sets

    Args:
        code (string): The 3 letter code of the set
        format (string, optional):
            Returns data in the specified method. Defaults to JSON.
        pretty (string, optional):
            Returns a prettier version of the json object. Note that this may break functionality with Scrython.

    Returns:
        N/A

    Raises:
        N/A

    Examples:
        >>> set = scrython.sets.Sets()
        >>> set.data(3, "name")
    """
    def __init__(self):
        self._url = 'sets?'
        super(Sets, self).__init__(self._url)

    def object(self):
        """Returns the type of object it is
        (card, error, etc)
        
        Returns:
            string
        """
        super(Sets, self)._checkForKey('object')

        return self.scryfallJson['object']

    def has_more(self):
        """True if there are more pages available
        
        Returns:
            boolean
        """
        super(Sets, self)._checkForKey('has_more')

        return self.scryfallJson['has_more']

    def data(self, index=None, key=None):
        """The data returned from the query

        Acceptable keys:
            object (string): The set object.
            code (string): The three letter set code of the set.
            mtgo_code (string): The mtgo equivalent of `code()`.
            name (string): The full name of the set.
            set_type (string): The type of the set (expansion, commander, etc)
            released_at (string): The date the set was launched.
            block_code (string): The the letter code for the block the set was in.
            block (string): The full name of the block a set was in.
            parent_set_code (string): The set code for the parent set.
            card_count (integer): The number of cards in the set.
            digital (boolean): True if this set is only featured on MTGO.
            foil_only (boolean): True if this set only has foils.
            icon_svg_uri (string): A URI to the SVG of the set symbol.
            search_uri (string): The scryfall API url for the search.

        Args:
            index (integer, optional): Defaults to None. Access a specific index.
            key (string, optional): Defaults to None. Returns the value of the given key. Requires the `index` argument.
        
        Returns:
            List: The full list of data.
            Dictionary: If given an index
            String: If given an index and key.
        """
        super(Sets, self)._checkForKey('data')

        if index is not None:
            if key is not None:
                super(Sets, self)._checkForTupleKey('data', index, key)
                return self.scryfallJson['data'][index][key]

            return self.scryfallJson['data'][index]

        return self.scryfallJson['data']

    def data_length(self):
        """The length of the data returned
        
        Returns:
            integer
        """
        super(Sets, self)._checkForKey('data')

        return len(self.scryfallJson['data'])