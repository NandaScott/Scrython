from .catalogs_object import CatalogsObject

class CreatureTypes(CatalogsObject):
    """
    catalogs/creature-types

    Catalog object for all known creature types.

    Example usage:
        >>> catalog = scrython.catalog.CreatureTypes()
        >>> catalog.data()
    """
    def __init__(self):
        self._url = 'catalog/creature-types?'
        super(CreatureTypes, self).__init__(self._url)
