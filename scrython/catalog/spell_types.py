from .catalogs_object import CatalogsObject

class SpellTypes(CatalogsObject):
    def __init__(self):
        self._url = 'catalog/spell-types?'
        super(SpellTypes, self).__init__(self._url)
