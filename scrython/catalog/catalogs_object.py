import sys
sys.path.append('..')
from scrython.foundation import FoundationObject

class CatalogsObject(FoundationObject):
    """
    Master object for all catalog objects.

    Args:
        format (string, optional):
            Defaults to 'json'.
            Returns data in the specified method.
        pretty (string, optional):
            Defaults to empty string.
            Returns a prettier version of the json object.
            Note that this may break functionality with Scrython.

    Returns:
        N/A

    Raises:
        N/A

    Examples:
        N/A
    """

    def object(self):
        """Returns the type of object it is
        (card, error, etc)
        
        Returns:
            string
        """
        super(CatalogsObject, self)._checkForKey('object')

        return self.scryfallJson['object']

    def uri(self):
        """The API URI for the endpoint you've called.
        
        Returns:
            string
        """
        super(CatalogsObject, self)._checkForKey('uri')

        return self.scryfallJson['uri']

    def total_values(self):
        """The number of items in `data()`
        
        Returns:
            integer
        """
        super(CatalogsObject, self)._checkForKey('total_values')

        return self.scryfallJson['total_values']

    def data(self):
        """A list of all types returned by the endpoint
        
        Returns:
            list
        """
        super(CatalogsObject, self)._checkForKey('data')

        return self.scryfallJson['data']
