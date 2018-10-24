from .catalogs_object import CatalogsObject

class PlaneswalkerTypes(CatalogsObject):
    """
    catalogs/planeswalker-types

    Catalog object for all known planeswalker types.

    Example usage:
        >>> catalog = scrython.catalog.PlaneswalkerTypes()
        >>> catalog.data()
    """
    def __init__(self):
        self._url = 'catalog/planeswalker-types?'
        super(PlaneswalkerTypes, self).__init__(self._url)
