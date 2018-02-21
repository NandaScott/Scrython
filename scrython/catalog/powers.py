from .catalogs_object import CatalogsObject

class Powers(CatalogsObject):
    """
    catalogs/powers

    Catalog object for all known powers.

    Positional Arguments:
        No arguments are required.

    Optional Arguments:
        All arguments are inherited from CatalogsObject

    Attributes:
        All attributes are inherited from CatalogsObject

    Example usage:
        >>> catalog = scrython.catalog.Powers()
        >>> catalog.data()
    """
    def __init__(self):
        self._url = 'catalog/powers?'
        super(Powers, self).__init__(self._url)
