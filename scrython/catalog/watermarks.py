from .catalogs_object import CatalogsObject

class Watermarks(CatalogsObject):
    def __init__(self):
        self._url = 'catalog/watermarks?'
        super(Watermarks, self).__init__(self._url)
