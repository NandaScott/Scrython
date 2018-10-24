import sys
sys.path.append('..')
from scrython.foundation import FoundationObject
import asyncio
import aiohttp
import urllib.parse
from threading import Thread

class CatalogsObject(FoundationObject):
    """
    Master object for all catalog objects.

    Positional Arguments:
        No arguments are required.

    Optional Arguments:
        format : str ................... The format to return. Defaults to JSON.
        pretty : bool ... Makes the returned JSON prettier. The library may not work properly with this setting.

    Attributes:
        object : str ...... Returns the type of object it is. (card, error, etc)
        uri : str .................. The API URI for the endpoint you've called.
        total_values : int ..................... The number of items in `data()`
        data : list .............. A list of all types returned by the endpoint.
    """

    def object(self):
        super(CatalogsObject, self)._checkForKey('object')

        return self.scryfallJson['object']

    def uri(self):
        super(CatalogsObject, self)._checkForKey('uri')

        return self.scryfallJson['uri']

    def total_values(self):
        super(CatalogsObject, self)._checkForKey('total_values')

        return self.scryfallJson['total_values']

    def data(self):
        super(CatalogsObject, self)._checkForKey('data')

        return self.scryfallJson['data']
