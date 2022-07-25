from .catalogs_object import CatalogsObject


class AbilityWords(CatalogsObject):
    """
    catalogs/ability-words

    Catalog object for all known ability words

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
        self._url = 'catalog/ability-words?'
        super(AbilityWords, self).__init__(self._url)
