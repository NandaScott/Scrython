from .catalogs_object import CatalogsObject

class Powers(CatalogsObject):
    def __init__(self):
        self._url = 'catalog/powers?'
        super(Powers, self).__init__(self._url)
