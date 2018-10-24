from .catalogs_object import CatalogsObject

class SpellTypes(CatalogsObject):
    """
    catalogs/spell-types

    Catalog object for all known spell types.

    Example usage:
        >>> catalog = scrython.catalog.SpellTypes()
        >>> catalog.data()
    """
    def __init__(self):
        self._url = 'catalog/spell-types?'
        super(SpellTypes, self).__init__(self._url)
