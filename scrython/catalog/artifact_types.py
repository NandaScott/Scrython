from .catalogs_object import CatalogsObject

class ArtifactTypes(CatalogsObject):
    """
    catalogs/artifact-types

    Catalog object for all known artifact types

    Example usage:
        >>> catalog = scrython.catalog.ArtifactTypes()
        >>> catalog.data()
    """
    def __init__(self):
        self._url = 'catalog/artifact-types?'
        super(ArtifactTypes, self).__init__(self._url)
