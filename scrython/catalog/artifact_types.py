from .catalogs_object import CatalogsObject

class ArtifactTypes(CatalogsObject):
    def __init__(self):
        self._url = 'catalog/artifact-types?'
        super(ArtifactTypes, self).__init__(self._url)
