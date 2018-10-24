import asyncio
import aiohttp
import urllib.parse
from threading import Thread

class BulkData(object):
    """
    /bulk-data
    Queries and creates an object relating to the /bulk-data endpoint.
    
    Raises:
        Exception: Raised if Scryfall sends an error object.
        KeyError: Raised if you attempt to access a key that doesn't exist.
        KeyError: Raise if you attempt to access a tuple key that doesn't exist.
    
    Returns:
        object: The Scryfall endpoint object.
    """
    def __init__(self, **kwargs):

        self._url = 'https://api.scryfall.com/bulk-data'

        async def getRequest(client, url, **kwargs):
            async with client.get(url, **kwargs) as response:
                return await response.json()

        async def main(loop):
            async with aiohttp.ClientSession(loop=loop) as client:
                self.scryfallJson = await getRequest(client, self._url)

        def do_everything():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(main(loop))

        t = Thread(target=do_everything)
        t.run()

        if self.scryfallJson['object'] == 'error':
            raise Exception(self.scryfallJson['details'])

    def _checkForKey(self, key):
        """Checks for a key in the scryfallJson object.
        This function should be considered private, and
        should not be accessed in production.
        
        Args:
            key (string): The key to check
        
        Raises:
            KeyError: If key is not found.
        """
        if not key in self.scryfallJson:
            raise KeyError('This card has no key \'{}\''.format(key))

    def _checkForTupleKey(self, parent, num, key):
        """Checks for a key of an object in an array.
        This function should be considered private, and
        should not be accessed in production.
        
        Args:
            parent (string): The key for the array to be accessed
            num (int): The index of the array
            key (string): The key to check
        
        Raises:
            KeyError: If key is not found.
        """
        if not key in self.scryfallJson[parent][num]:
            raise KeyError('This tuple has no key \'{}\''.format(key))

    def object(self):
        """Returns the type of object it is.
        (card, error, etc)
        
        Returns:
            string: The type of object
        """
        self._checkForKey('object')

        return self.scryfallJson['object']

    def has_more(self):
        """True if there is more than one page of results
        
        Returns:
            boolean: True if there are more results
        """
        self._checkForKey('has_more')

        return self.scryfallJson['has_more']

    def data(self):
        """A list of all types of types returned by the endpoints
        
        Returns:
            list: List of all types
        """
        self._checkForKey('data')

        return self.scryfallJson['data']

    def bulk_object(self, num):
        """Returns the type of object the specified index is
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: The type of object
        """
        self._checkForTupleKey('data', num, 'object')

        return self.scryfallJson['data'][num]['object']

    def bulk_id(self, num):
        """The unique ID of the bulk item
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: The Scryfall id of the object
        """
        self._checkForTupleKey('data', num, 'id')

        return self.scryfallJson['data'][num]['id']

    def bulk_type(self, num):
        """The type of bulk data
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: The type of the data item
        """
        self._checkForTupleKey('data', num, 'type')

        return self.scryfallJson['data'][num]['type']

    def bulk_updated_at(self, num):
        """The time the item was last updated
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: Timestamp
        """
        self._checkForTupleKey('data', num, 'updated_at')

        return self.scryfallJson['data'][num]['updated_at']

    def bulk_name(self, num):
        """The name of the type of bulk data object
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: The name of the data item
        """
        self._checkForTupleKey('data', num, 'name')

        return self.scryfallJson['data'][num]['name']

    def bulk_description(self, num):
        """A description of the object
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: The description of the data item
        """
        self._checkForTupleKey('data', num, 'description')

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
        self._checkForTupleKey('data', num, 'compressed_size')

        if human_readable:
            before = self.scryfallJson['data'][num]['compressed_size']

            for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB']:
                if abs(before) < 1024.0:
                    return '{:3.1f}{}'.format(before, unit)
                before /= 1024.0

            return '{:.1f}{}'.format(before, 'YiB')

        return self.scryfallJson['data'][num]['compressed_size']

    def bulk_permalink_uri(self, num):
        """The URL that hosts the bulk file
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: A URI to download the compressed data
        """
        self._checkForTupleKey('data', num, 'permalink_uri')

        return self.scryfallJson['data'][num]['permalink_uri']

    def bulk_content_type(self, num):
        """The MIME type of the file
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: The MIME type
        """
        self._checkForTupleKey('data', num, 'content_type')

        return self.scryfallJson['data'][num]['content_type']

    def bulk_content_encoding(self, num):
        """The encoding of the file
        
        Args:
            num (int): The index of the object in the `data` key
        
        Returns:
            string: The encoding of the file
        """
        self._checkForTupleKey('data', num, 'content_encoding')

        return self.scryfallJson['data'][num]['content_encoding']
