from .catalogs_object import CatalogsObject

class Toughnesses(CatalogsObject):
    """
    catalogs/toughnesses

    Catalog object for all known toughnesses.

    Example usage:
        >>> catalog = scrython.catalog.Toughnesses()
        >>> catalog.data()
    """
    def __init__(self):
        self._url = 'catalog/toughnesses?'
        super(Toughnesses, self).__init__(self._url)
