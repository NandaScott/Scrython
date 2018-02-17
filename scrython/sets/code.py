from .sets_object import SetsObject

class Code(SetsObject):
    def __init__(self, code):
        self._url = 'sets/{}?'.format(code)
        super(Code, self).__init__(self._url)
