import asyncio
import aiohttp
import urllib.parse
from threading import Thread

class BulkData(object):
    """
    Master object for all bulk data objects.

    Positional Arguments:
        No arguments are required.

    Attributes:
        object : str ...... Returns the type of object it is. (card, error, etc)
        total_values : int ..................... The number of items in `data()`
        has_more : bool ........ True if there is more than one page of results.
        data : list .............. A list of all types returned by the endpoint.
        bulk_object(num) : str .. Returns the type of object the specified tuple is
        bulk_id(num) : str ..................... The unique ID of the bulk item
        bulk_type(num) : str ............................ The type of bulk data
        bulk_updated_at(num) : str ......... The time the item was last updated
        bulk_name(num) : str ......... The name of the type of bulk data object
        bulk_description(num) : str ............... A description of the object
        bulk_compressed_size(num) : int ......... The size of the file in bytes
        bulk_permalink_uri(num) : str ........ The URL that hosts the bulk file
        bulk_content_type(num) : str ................ The MIME type of the file
        bulk_content_encoding(num) : str ............. The encoding of the file
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
        if not key in self.scryfallJson:
            raise KeyError('This card has no key \'{}\''.format(key))

    def _checkForTupleKey(self, parent, num, key):
        if not key in self.scryfallJson[parent][num]:
            raise KeyError('This tuple has no key \'{}\''.format(key))

    def object(self):
        self._checkForKey('object')

        return self.scryfallJson['object']

    def has_more(self):
        self._checkForKey('has_more')

        return self.scryfallJson['has_more']

    def data(self):
        self._checkForKey('data')

        return self.scryfallJson['data']

    def bulk_object(self, num):
        self._checkForTupleKey('data', num, 'object')

        return self.scryfallJson['data'][num]['object']

    def bulk_id(self, num):
        self._checkForTupleKey('data', num, 'id')

        return self.scryfallJson['data'][num]['id']

    def bulk_type(self, num):
        self._checkForTupleKey('data', num, 'type')

        return self.scryfallJson['data'][num]['type']

    def bulk_updated_at(self, num):
        self._checkForTupleKey('data', num, 'updated_at')

        return self.scryfallJson['data'][num]['updated_at']

    def bulk_name(self, num):
        self._checkForTupleKey('data', num, 'name')

        return self.scryfallJson['data'][num]['name']

    def bulk_description(self, num):
        self._checkForTupleKey('data', num, 'description')

        return self.scryfallJson['data'][num]['description']

    def bulk_compressed_size(self, num, human_readable=False):
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
        self._checkForTupleKey('data', num, 'permalink_uri')

        return self.scryfallJson['data'][num]['permalink_uri']

    def bulk_content_type(self, num):
        self._checkForTupleKey('data', num, 'content_type')

        return self.scryfallJson['data'][num]['content_type']

    def bulk_content_encoding(self, num):
        self._checkForTupleKey('data', num, 'content_encoding')

        return self.scryfallJson['data'][num]['content_encoding']
