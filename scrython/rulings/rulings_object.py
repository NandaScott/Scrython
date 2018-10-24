import sys
sys.path.append('..')
from scrython.foundation import FoundationObject
import asyncio
import aiohttp
import urllib.parse
from threading import Thread

class RulingsObject(FoundationObject):
    """
    Master class for all rulings objects.

    Positional arguments:
        No arguments required.

    Optional arguments:
        format : str ... Returns data in the specified method. Defaults to JSON.
        face : str ... If you're using the `image` format, this will specify if
                        you want the front or back face.
        version : str ... If you're using the `image` format, this will specify if
                        you want the small, normal, large, etc version of the image.
        pretty : str ... Returns a prettier version of the json object. Note that
                          this may break functionality with Scrython.

    Attributes:
        object : str ...... Returns the type of object it is. (card, error, etc)
        had_more : bool ... If true, this ruling object has more rules than it currently displays.
        data : list .................................. A list of ruling objects.
        data_length : int ....................... The length of the `data` list.

        The following require an integer as an arg, which acts as a tuple.
        ruling_object : str ............. The type of object for a given ruling.
        ruling_source : str .......................... The source of the ruling.
        ruling_published_at : str ...... The date when the ruling was published.
        ruling_comment : str ............................. The effective ruling.
    """

    def _checkForKey(self, key):
        if not key in self.scryfallJson:
            raise KeyError('This object has no key \'{}\''.format(key))

    def _checkForTupleKey(self, parent, num, key):
        if not key in self.scryfallJson[parent][num]:
            raise KeyError('This ruling has no key \'{}\''.format(key))

    def object(self):
        self._checkForKey('object')

        return self.scryfallJson['object']

    def has_more(self):
        self._checkForKey('has_more')

        return self.scryfallJson['has_more']

    def data(self, index=None, key=None):
        self._checkForKey('data')

        if index is not None:
            if key is not None:
                self._checkForTupleKey('data', index, key)
                return self.scryfallJson['data'][index][key]

            return self.scryfallJson['data'][index]

        return self.scryfallJson['data']

    def data_length(self):
        self._checkForKey('data')

        return len(self.scryfallJson['data'])

    def ruling_object(self, num):
        self._checkForTupleKey('data', num, 'object')

        return self.scryfallJson['data'][num]['object']

    def ruling_source(self, num):
        self._checkForTupleKey('data', num, 'source')

        return self.scryfallJson['data'][num]['source']

    def ruling_published_at(self, num):
        self._checkForTupleKey('data', num, 'published_at')

        return self.scryfallJson['data'][num]['published_at']

    def ruling_comment(self, num):
        self._checkForTupleKey('data', num, 'comment')

        return self.scryfallJson['data'][num]['comment']
