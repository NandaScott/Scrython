from .catalogs_object import CatalogsObject

class CreatureTypes(CatalogsObject):
    def __init__(self):
        self._url = 'catalog/creature-types?'
        super(CreatureTypes, self).__init__(self._url)
