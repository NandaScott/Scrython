from .catalogs_object import CatalogsObject

class PlaneswalkerTypes(CatalogsObject):
    def __init__(self):
        self._url = 'catalog/planeswalker-types?'
        super(PlaneswalkerTypes, self).__init__(self._url)
