from .catalogs_object import CatalogsObject

class WordBank(CatalogsObject):
    """
    catalogs/word-bank

    Catalog object for all known words on all cards.

    Positional Arguments:
        No arguments are required.

    Optional Arguments:
        All arguments are inherited from CatalogsObject

    Attributes:
        All attributes are inherited from CatalogsObject

    Example usage:
        >>> catalog = scrython.catalog.WordBank()
        >>> catalog.data()
    """
    def __init__(self):
        self._url = 'catalog/word-bank?'
        super(WordBank, self).__init__(self._url)
