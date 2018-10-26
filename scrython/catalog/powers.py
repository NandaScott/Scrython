from .catalogs_object import CatalogsObject

class Powers(CatalogsObject):
    """
    catalogs/powers

    Catalog object for all known powers.

    Args:
        N/A

    Returns:
        N/A

    Raises:
        N/A

    Examples:
        >>> catalog = scrython.catalog.Powers()
        >>> catalog.data()
    """
    def __init__(self):
        self._url = 'catalog/powers?'
        super(Powers, self).__init__(self._url)
