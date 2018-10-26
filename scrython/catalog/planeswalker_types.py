from .catalogs_object import CatalogsObject

class PlaneswalkerTypes(CatalogsObject):
    """
    catalogs/planeswalker-types

    Catalog object for all known planeswalker types.

    Args:
        N/A

    Returns:
        N/A

    Raises:
        N/A

    Examples:
        >>> catalog = scrython.catalog.PlaneswalkerTypes()
        >>> catalog.data()
    """
    def __init__(self):
        self._url = 'catalog/planeswalker-types?'
        super(PlaneswalkerTypes, self).__init__(self._url)
