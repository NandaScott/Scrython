from .sets_object import SetsObject

class Code(SetsObject):
    """
    sets/:code
    Get a set with a 3 letter code.

    Positional arguments:
        code : str ............................... The 3 letter code of the set.

    Optional arguments:
        All arguments are inherited from SetsObject

    Attributes:
        All attributes are inherited from SetsObject

    Example usage:
        >>> set = scrython.sets.Code(code='por')
        >>> set.name()
    """
    def __init__(self, code):
        self._url = 'sets/{}?'.format(code)
        super(Code, self).__init__(self._url)
