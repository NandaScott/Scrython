from .catalogs_object import CatalogsObject

class WordBank(CatalogsObject):
    def __init__(self):
        self._url = 'catalog/word-bank?'
        super(WordBank, self).__init__(self._url)
