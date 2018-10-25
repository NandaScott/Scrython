import sys
sys.path.append('..')
from scrython.foundation import FoundationObject

class RulingsObject(FoundationObject):
    """
    Master class for all rulings objects.

    Args:
        format (string, optional): Returns data in the specified method. Defaults to JSON.
        face (string, optional): 
            If you're using the `image` format, this will specify if you want the front or back face.
        version (string, optional):
            If you're using the `image` format, this will specify if you want the small, normal, large, etc version of the image.
        pretty (string, optional):
            Returns a prettier version of the json object. Note that this may break functionality with Scrython.

    """

    def object(self):
        """Returns the type of object it is
        (card, error, etc)
        
        Returns:
            string
        """
        super(RulingsObject, self)._checkForKey('object')

        return self.scryfallJson['object']

    def has_more(self):
        """True if there is more than one page of results
        
        Returns:
            boolean: True if there are more results
        """
        super(RulingsObject, self)._checkForKey('has_more')

        return self.scryfallJson['has_more']

    def data(self, index=None, key=None):
        """The data returned from the query

        Acceptable keys:
            object (string): The type of object for a given ruling.
            source (string): The source of the ruling.
            published_at (string): The date when the ruling was published.
            comment (string): The effective ruling.

        Args:
            index (integer, optional): Defaults to None. Access a specific index.
            key (string, optional): Defaults to None. Returns the value of the given key. Requires the `index` argument.
        
        Returns:
            List: The full list of data.
            Dictionary: If given an index
            String: If given an index and key.
        """
        super(RulingsObject, self)._checkForKey('data')

        if index is not None:
            if key is not None:
                super(RulingsObject, self)._checkForTupleKey('data', index, key)
                return self.scryfallJson['data'][index][key]

            return self.scryfallJson['data'][index]

        return self.scryfallJson['data']

    def data_length(self):
        """The length of the `data` list.
        
        Returns:
            Integer
        """
        super(RulingsObject, self)._checkForKey('data')

        return len(self.scryfallJson['data'])
