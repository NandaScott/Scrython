import aiohttp
import asyncio
import urllib

class ScryfallError(Exception):
    def __init__(self, error_obj, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.error_details = {}
        self.error_details.update(error_obj)


class FoundationObject(object):

    def __init__(self, _url, override=False, **kwargs):
        self.params = {
            'format': kwargs.get('format', 'json'), 'face': kwargs.get('face', ''),
            'version': kwargs.get('version', ''), 'pretty': kwargs.get('pretty', '')
        }

        self.encodedParams = urllib.parse.urlencode(self.params)
        self._url = 'https://api.scryfall.com/{0}&{1}'.format(_url, self.encodedParams)

        if override:
            self._url = _url

        async def getRequest(client, url, **kwargs):
            async with client.get(url, **kwargs) as response:
                return await response.json()

        async def main(loop):
            async with aiohttp.ClientSession(loop=loop) as client:
                self.scryfallJson = await getRequest(client, self._url)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(loop))

        if self.scryfallJson['object'] == 'error':
            raise ScryfallError(self.scryfallJson, self.scryfallJson['details'])

    def _checkForKey(self, key, nested_key=None):
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

        if nested_key:
            if not nested_key in self.scryfallJson[key]:
                raise KeyError('This card has no key \'{}.{}\''.format(key, nested_key))


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
