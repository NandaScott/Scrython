from .catalogs_object import CatalogsObject


class KeywordAbilities(CatalogsObject):
    """
    catalog/keyword-abilities

    Catalog object for all known keyword abilities

    Args:
        N/A

    Returns:
        N/A

    Raises:
        N/A

    Examples:
        >>> catalog = scrython.catalog.KeywordAbilities()
        >>> catalog.data()
    """

    def __init__(self):
        self._url = 'catalog/keyword-abilities?'
        super(KeywordAbilities, self).__init__(self._url)
