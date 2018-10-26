import sys
sys.path.append('..')
from scrython.foundation import FoundationObject
import urllib.parse

class Autocomplete(FoundationObject):
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

    Returns:
        N/A

    Raises:
        Exception: If the 'q' parameter is not provided.
        Exception: If the object returned is an error.

    Examples:
        >>> auto = scrython.cards.Autocomplete(q="Thal")
        >>> auto.total_items()
    """
    def __init__(self, **kwargs):
        if kwargs.get('q') is None:
            raise Exception('No query provided to search by')

        self.dict = { 'q': kwargs.get('q') }

        self.args = urllib.parse.urlencode(self.dict)
        self.url = 'cards/autocomplete?' + self.args
        super(Autocomplete, self).__init__(self.url)

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