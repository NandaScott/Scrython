from .catalogs_object import CatalogsObject


class KeywordActions(CatalogsObject):
    """
    catalog/keyword-actions

    Catalog object for all known keyword actions

    Args:
        N/A

    Returns:
        N/A

    Raises:
        N/A

    Examples:
        >>> catalog = scrython.catalog.KeywordActions()
        >>> catalog.data()
    """

    def __init__(self):
        self._url = 'catalog/keyword-actions?'
        super(KeywordActions, self).__init__(self._url)
