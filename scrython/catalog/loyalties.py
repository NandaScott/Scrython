from .catalogs_object import CatalogsObject

class Loyalties(CatalogsObject):
    def __init__(self):
        self._url = 'catalog/loyalties?'
        super(Loyalties, self).__init__(self._url)
