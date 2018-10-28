import sys
sys.path.append('..')
from scrython.foundation import FoundationObject

class Symbology(FoundationObject):
    """
    /symbology

    Args:
        N/A

    Returns:
        N/A

    Raises:
        N/A

    Examples:
        >>> symbol = scrython.symbology.Symbology()
    """
    def __init__(self):
        self.url = 'symbology?'
        super(Symbology, self).__init__(self.url)

    def object(self):
        """Returns the type of object it is
        (card, error, etc)

        Returns:
            string
        """
        super(Symbology, self)._checkForKey('object')

        return self.scryfallJson['object']

    def has_more(self):
        """True if there are more pages to the object
        
        Returns:
            boolean
        """
        super(Symbology, self)._checkForKey('has_more')

        return self.scryfallJson['has_more']

    def data(self, index=None, key=None):
        """The data returned from the query

        Acceptable keys:
            symbol (string): The plaintext symbol, usually written with curly braces
            loose_variant (string): The alternate version of the symbol, without curly braces
            transposable (boolean): True if it's possibly to write the symbol backwards
            represents_mana (boolean): True if this is a mana symbol
            cmc (float): The total converted mana cost of the symbol
            appears_in_mana_costs (boolean): True if the symbol appears on the mana cost of any card
            funny (boolean): True if the symbol is featured on any funny cards
            colors (array): An array of all colors in the given symbol
            english (string): An english sentence describing the mana cost
            gatherer_alternate (array): An array of Gatherer like costs

        Args:
            index (integer, optional): Defaults to None. Access a specific index.
            key (string, optional): Defaults to None. Returns the value of the given key. Requires the `index` argument.

        Returns:
            List: The full list of data.
            Dictionary: If given an index
            String: If given an index and key.
        """
        super(Symbology, self)._checkForKey('has_more')

        if index is not None:
            if key is not None:
                super(Symbology, self)._checkForTupleKey('data', index, key)
                return self.scryfallJson['data'][index][key]

            return self.scryfallJson['data'][index]

        return self.scryfallJson['data']

    def data_length(self):
        """The length of the data returned
        
        Returns:
            integer
        """
        super(Symbology, self)._checkForKey('data')

        return len(self.scryfallJson['data'])