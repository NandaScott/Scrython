from .catalogs_object import CatalogsObject

class Watermarks(CatalogsObject):
    """
    catalogs/watermarks

    Catalog object for all known watermarks.

    Positional Arguments:
        No arguments are required.

    Optional Arguments:
        All arguments are inherited from CatalogsObject

    Attributes:
        All attributes are inherited from CatalogsObject

    Example usage:
        >>> catalog = scrython.catalog.Watermarks()
        >>> catalog.data()
    """
    def __init__(self):
        self._url = 'catalog/watermarks?'
        super(Watermarks, self).__init__(self._url)
