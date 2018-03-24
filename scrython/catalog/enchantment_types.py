from .catalogs_object import CatalogsObject

class EnchantmentTypes(CatalogsObject):
    """
    catalogs/enchantment-types

    Catalog object for all known enchantment types.

    Positional Arguments:
        No arguments are required.

    Optional Arguments:
        All arguments are inherited from CatalogsObject

    Attributes:
        All attributes are inherited from CatalogsObject

    Example usage:
        >>> catalog = scrython.catalog.EnchantmentTypes()
        >>> catalog.data()
    """
    def __init__(self):
        self._url = 'catalog/enchantment-types?'
        super(EnchantmentTypes, self).__init__(self._url)
