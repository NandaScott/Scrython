from .catalogs_object import CatalogsObject

class Watermarks(CatalogsObject):
    """
    catalogs/watermarks

    Catalog object for all known watermarks.

    Args:
        N/A

    Returns:
        N/A

    Raises:
        N/A

    Examples:
        >>> catalog = scrython.catalog.Watermarks()
        >>> catalog.data()
    """
    def __init__(self):
        self._url = 'catalog/watermarks?'
        super(Watermarks, self).__init__(self._url)
