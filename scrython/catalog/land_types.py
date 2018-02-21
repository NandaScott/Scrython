from .catalogs_object import CatalogsObject

class LandTypes(CatalogsObject):
    """
    catalogs/land-types

    Catalog object for all known land types.

    Positional Arguments:
        No arguments are required.

    Optional Arguments:
        All arguments are inherited from CatalogsObject

    Attributes:
        All attributes are inherited from CatalogsObject

    Example usage:
        >>> catalog = scrython.catalog.LandTypes()
        >>> catalog.data()
    """
    def __init__(self):
        self._url = 'catalog/land-types?'
        super(LandTypes, self).__init__(self._url)
