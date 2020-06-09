import sys
sys.path.append('..')
from scrython.foundation import FoundationObject
import asyncio
import aiohttp
import urllib.parse
from threading import Thread
import warnings

class BulkData(FoundationObject):
    """
    /bulk-data
    Queries and creates an object relating to the /bulk-data endpoint.

    Args:
        N/A

    Returns:
        object: The Scryfall endpoint object.

    Raises:
        Exception: Raised if Scryfall sends an error object.

    Examples:
        >>> data = scrython.bulk_data.BulkData()
        >>> data.bulk_compressed_size()
    """
    def __init__(self, **kwargs):

        self.url = 'https://api.scryfall.com/bulk-data'
        super(BulkData, self).__init__(self.url, True)

    def object(self):
        """Returns the type of object it is.
        (card, error, etc)
        
        Returns:
            string: The type of object
        """
        super(BulkData, self)._checkForKey('object')

        return self.scryfallJson['object']

    def has_more(self):
        """True if there is more than one page of results
        
        Returns:
            boolean: True if there are more results
        """
        super(BulkData, self)._checkForKey('has_more')

        return self.scryfallJson['has_more']

    def data(self):
        """A list of all types of types returned by the endpoints
        
        Returns:
            list: List of all types
        """
        super(BulkData, self)._checkForKey('data')

        return self.scryfallJson['data']

    def bulk_object(self, num):
        """Returns the type of object the specified index is
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: The type of object
        """
        super(BulkData, self)._checkForTupleKey('data', num, 'object')

        return self.scryfallJson['data'][num]['object']

    def bulk_id(self, num):
        """The unique ID of the bulk item
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: The Scryfall id of the object
        """
        super(BulkData, self)._checkForTupleKey('data', num, 'id')

        return self.scryfallJson['data'][num]['id']

    def bulk_type(self, num):
        """The type of bulk data
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: The type of the data item
        """
        super(BulkData, self)._checkForTupleKey('data', num, 'type')

        return self.scryfallJson['data'][num]['type']

    def bulk_updated_at(self, num):
        """The time the item was last updated
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: Timestamp
        """
        super(BulkData, self)._checkForTupleKey('data', num, 'updated_at')

        return self.scryfallJson['data'][num]['updated_at']

    def bulk_name(self, num):
        """The name of the type of bulk data object
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: The name of the data item
        """
        super(BulkData, self)._checkForTupleKey('data', num, 'name')

        return self.scryfallJson['data'][num]['name']

    def bulk_description(self, num):
        """A description of the object
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: The description of the data item
        """
        super(BulkData, self)._checkForTupleKey('data', num, 'description')

        return self.scryfallJson['data'][num]['description']

    def bulk_compressed_size(self, num, human_readable=False):
        """The size of the file in bytes
        
        Args:
            num (int): The index of the object in the `data` key
            human_readable (bool, optional): Defaults to False. Converts the bytes into a human readable format
        
        Returns:
            integer: Returns integer by default. 
            string: If human_readable is True, returns a string.
        """
        super(BulkData, self)._checkForTupleKey('data', num, 'compressed_size')

        if human_readable:
            before = self.scryfallJson['data'][num]['compressed_size']

            for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB']:
                if abs(before) < 1024.0:
                    return '{:3.1f}{}'.format(before, unit)
                before /= 1024.0

            return '{:.1f}{}'.format(before, 'YiB')

        return self.scryfallJson['data'][num]['compressed_size']

    def bulk_permalink_uri(self, num):
        warnings.warn("This method has been renamed to bulk_uri as per https://scryfall.com/blog/updates-to-bulk-data-and-cards-deprecation-notice-217", DeprecationWarning)
        return self.bulk_uri(num)

    def bulk_uri(self, num):
        """The URL that hosts the bulk file
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: A URI to download the compressed data
        """
        super(BulkData, self)._checkForTupleKey('data', num, 'uri')

        return self.scryfallJson['data'][num]['uri']

    def bulk_content_type(self, num):
        """The MIME type of the file
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: The MIME type
        """
        super(BulkData, self)._checkForTupleKey('data', num, 'content_type')

        return self.scryfallJson['data'][num]['content_type']

    def bulk_content_encoding(self, num):
        """The encoding of the file
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: The encoding of the file
        """
        super(BulkData, self)._checkForTupleKey('data', num, 'content_encoding')

        return self.scryfallJson['data'][num]['content_encoding']
