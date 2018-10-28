import sys
sys.path.append('..')
from scrython.foundation import FoundationObject

class ParseMana(FoundationObject):
    """
    symbology/parse-mana

    Args:
        cost (string): The given mana cost you want. (`RUG`)
        format (string, optional):
            Returns data in the specified method. Defaults to JSON.
        pretty (string, optional):
            Returns a prettier version of the json object. Note that this may break functionality with Scrython.

    Returns:
        N/A

    Raises:
        N/A

    Examples:
        >>> mana = scrython.symbology.ParseMana(cost="xcug")
        >>> mana.colors()
    """
    def __init__(self, cost):
        self.cost = cost
        self.url = 'symbology/parse-mana?cost=' + self.cost
        super(ParseMana, self).__init__(self.url)

    def object(self):
        """Returns the type of object it is
        (card, error, etc)

        Returns:
            string
        """
        super(ParseMana, self)._checkForKey('object')

        return self.scryfallJson['object']

    def mana_cost(self):
        """The formatted mana cost
        
        Returns:
            string
        """
        super(ParseMana, self)._checkForKey('cost')

        return self.scryfallJson['cost']

    def cmc(self):
        """The converted mana cost of the card 
        
        Returns:
            float
        """
        super(ParseMana, self)._checkForKey('cmc')

        return self.scryfallJson['cmc']

    def colors(self):
        """A list of all colors in the mana cost
        
        Returns:
            list
        """
        super(ParseMana, self)._checkForKey('colors')

        return self.scryfallJson['colors']

    def colorless(self):
        """True if the mana cost is colorless
        
        Returns:
            boolean
        """
        super(ParseMana, self)._checkForKey('colorless')

        return self.scryfallJson['colorless']

    def monocolored(self):
        """True if the mana cost is mono colored
        
        Returns:
            boolean
        """
        super(ParseMana, self)._checkForKey('monocolored')

        return self.scryfallJson['monocolored']

    def multicolored(self):
        """True if the mana cost is a multicolored cost
        
        Returns:
            boolean
        """
        super(ParseMana, self)._checkForKey('multicolored')

        return self.scryfallJson['multicolored']
