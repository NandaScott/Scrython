from .catalogs_object import CatalogsObject

class CardNames(CatalogsObject):
    def __init__(self):
        self._url = 'catalog/card-names?'
        super(CardNames, self).__init__(self._url)
