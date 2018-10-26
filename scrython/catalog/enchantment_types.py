from .catalogs_object import CatalogsObject

class EnchantmentTypes(CatalogsObject):
    """
    catalogs/enchantment-types

    Catalog object for all known enchantment types.

    Args:
        N/A

    Returns:
        N/A

    Raises:
        N/A

    Examples:
        >>> catalog = scrython.catalog.EnchantmentTypes()
        >>> catalog.data()
    """
    def __init__(self):
        self._url = 'catalog/enchantment-types?'
        super(EnchantmentTypes, self).__init__(self._url)
