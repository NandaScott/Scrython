from .catalogs_object import CatalogsObject

class Toughnesses(CatalogsObject):
    def __init__(self):
        self._url = 'catalog/toughnesses?'
        super(Toughnesses, self).__init__(self._url)
