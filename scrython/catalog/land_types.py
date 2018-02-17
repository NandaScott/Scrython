from .catalogs_object import CatalogsObject

class LandTypes(CatalogsObject):
    def __init__(self):
        self._url = 'catalog/land-types?'
        super(LandTypes, self).__init__(self._url)
