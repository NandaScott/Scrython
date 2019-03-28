import sys
sys.path.append('..')
from scrython.foundation import FoundationObject
from .cards_object import CardsObject
import urllib.parse

class Search(FoundationObject):
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

    Returns:
        N/A

    Raises:
        Exception: If the 'q' parameter is not provided.
        Exception: If the object returned is an error.

    Examples:
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
            'include_variations':kwargs.get('include_variations','false'),
            'include_extras':kwargs.get('include_extras', 'false'),
            'include_multilingual':kwargs.get('include_multilingual', 'false'),
            'page':kwargs.get('page', '1')
            }
        self.args = urllib.parse.urlencode(self.dict)
        self.url = 'cards/search?' + self.args

        super(Search, self).__init__(self.url)

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

    def data(self, index=None, key=None):
        """The data returned from the query

        You may reference any keys that could be accessed in a card object.
        There are far too many to list here, but you may find a list if applicable
        keys in the documentation.

        Args:
            index (integer, optional): Defaults to None. Access a specific index.
            key (string, optional): Defaults to None. Returns the value of the given key. Requires the `index` argument.
        
        Returns:
            List: The full list of data.
            Dictionary: If given an index.
            String: If given an index and key.
        """
        super(Search, self)._checkForKey('data')

        if index is not None:
            if key is not None:
                super(Search, self)._checkForTupleKey('data', index, key)
                return self.scryfallJson['data'][index][key]

            return self.scryfallJson['data'][index]

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

    def has_more(self):
        """Determines if there are more pages of results.
        
        Returns:
            boolean: True if there is more than 1 page of results
        """
        super(Search, self)._checkForKey('has_more')

        return self.scryfallJson['has_more']
