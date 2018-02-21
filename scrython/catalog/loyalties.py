from .catalogs_object import CatalogsObject

class Loyalties(CatalogsObject):
    """
    catalogs/loyalties

    Catalog object for all known starting loyalties.

    Positional Arguments:
        No arguments are required.

    Optional Arguments:
        All arguments are inherited from CatalogsObject

    Attributes:
        All attributes are inherited from CatalogsObject

    Example usage:
        >>> catalog = scrython.catalog.Loyalties()
        >>> catalog.data()
    """
    def __init__(self):
        self._url = 'catalog/loyalties?'
        super(Loyalties, self).__init__(self._url)
