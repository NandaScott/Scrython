from .catalogs_object import CatalogsObject

class CardNames(CatalogsObject):
    """
    catalogs/card-names

    Catalog object for all known card names.

    Positional Arguments:
        No arguments are required.

    Optional Arguments:
        All arguments are inherited from CatalogsObject

    Attributes:
        All attributes are inherited from CatalogsObject

    Example usage:
        >>> catalog = scrython.catalog.CardNames()
        >>> catalog.data()
    """
    def __init__(self):
        self._url = 'catalog/card-names?'
        super(CardNames, self).__init__(self._url)
