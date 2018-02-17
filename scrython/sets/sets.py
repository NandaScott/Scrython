from .sets_object import SetsObject

class Sets(SetsObject):
    def __init__(self):
        self._url = 'sets?'
        super(Sets, self).__init__(self._url)

    def __checkForKey(self, key):
        try:
            return self.scryfallJson[key]
        except KeyError:
            return None

    def __checkForTupleKey(self, parent, num, key):
        try:
            return self.scryfallJson[parent][num][key]
        except KeyError:
            return None

    def object(self):
        if self.__checkForKey('object') is None:
            raise KeyError('This object has no key \'object\'')

        return self.scryfallJson['object']

    def has_more(self):
        if self.__checkForKey('has_more') is None:
            return KeyError('This object has no key \'has_more\'')

        return self.scryfallJson['has_more']

    def data(self):
        if self.__checkForKey('data') is None:
            return KeyError('This object has no key \'data\'')

        return self.scryfallJson['data']

    def data_length(self):
        if self.__checkForKey('data') is None:
            return KeyError('This object has no key \'data\'')

        return len(self.scryfallJson['data'])

    def set_object(self, num):
        if self.__checkForTupleKey('data', num, 'object') is None:
            return KeyError('This ruling has no key \'object\'')

        return self.scryfallJson['data'][num]['object']

    def set_code(self, num):
        if self.__checkForTupleKey('data', num, 'code') is None:
            raise KeyError('This object has no key \'code\'')

        return self.scryfallJson['data'][num]['code']

    def set_mtgo_code(self, num):
        if self.__checkForTupleKey('data', num, 'mtgo_code') is None:
            raise KeyError('This object has no key \'mtgo_code\'')

        return self.scryfallJson['data'][num]['mtgo_code']

    def set_name(self, num):
        if self.__checkForTupleKey('data', num, 'name') is None:
            raise KeyError('This object has no key \'name\'')

        return self.scryfallJson['data'][num]['name']

    def set_set_type(self, num):
        if self.__checkForTupleKey('data', num, 'set_type') is None:
            raise KeyError('This object has no key \'set_type\'')

        return self.scryfallJson['data'][num]['set_type']

    def set_released_at(self, num):
        if self.__checkForTupleKey('data', num, 'released_at') is None:
            raise KeyError('This object has no key \'released_at\'')

        return self.scryfallJson['data'][num]['released_at']

    def set_block_code(self, num):
        if self.__checkForTupleKey('data', num, 'block_code') is None:
            raise KeyError('This object has no key \'block_code\'')

        return self.scryfallJson['data'][num]['block_code']

    def set_block(self, num):
        if self.__checkForTupleKey('data', num, 'block') is None:
            raise KeyError('This object has no key \'block\'')

        return self.scryfallJson['data'][num]['block']

    def set_parent_set_code(self, num):
        if self.__checkForTupleKey('data', num, 'parent_set_code') is None:
            raise KeyError('This object has no key \'parent_set_code\'')

        return self.scryfallJson['data'][num]['parent_set_code']

    def set_card_count(self, num):
        if self.__checkForTupleKey('data', num, 'card_count') is None:
            raise KeyError('This object has no key \'card_count\'')

        return self.scryfallJson['data'][num]['card_count']

    def set_digital(self, num):
        if self.__checkForTupleKey('data', num, 'digital') is None:
            raise KeyError('This object has no key \'digital\'')

        return self.scryfallJson['data'][num]['digital']

    def set_foil(self, num):
        if self.__checkForTupleKey('data', num, 'foil') is None:
            raise KeyError('This object has no key \'foil\'')

        return self.scryfallJson['data'][num]['foil']

    def set_icon_svg_uri(self, num):
        if self.__checkForTupleKey('data', num, 'icon_svg_uri') is None:
            raise KeyError('This object has no key \'icon_svg_uri\'')

        return self.scryfallJson['data'][num]['icon_svg_uri']

    def set_search_uri(self, num):
        if self.__checkForTupleKey('data', num, 'search_uri') is None:
            raise KeyError('This object has no key \'search_uri\'')

        return self.scryfallJson['data'][num]['search_uri']

	#The following attributes are only to override the inherited class attributes.
	#This class has no matching attributes but we still need the getRequest from SetsObject

    def code(self):
        raise AttributeError('This object has no key \'code\'')

    def mtgo_code(self):
        raise AttributeError('This object has no key \'mtgo_code\'')

    def name(self):
        raise AttributeError('This object has no key \'name\'')

    def set_type(self):
        raise AttributeError('This object has no key \'set_type\'')

    def released_at(self):
        raise AttributeError('This object has no key \'released_at\'')

    def block_code(self):
        raise AttributeError('This object has no key \'block_code\'')

    def block(self):
        raise AttributeError('This object has no key \'block\'')

    def parent_set_code(self):
        raise AttributeError('This object has no key \'parent_set_code\'')

    def card_count(self):
        raise AttributeError('This object has no key \'card_count\'')

    def digital(self):
        raise AttributeError('This object has no key \'digital\'')

    def foil(self):
        raise AttributeError('This object has no key \'foil\'')

    def icon_svg_uri(self):
        raise AttributeError('This object has no key \'icon_svg_uri\'')

    def search_uri(self):
        raise AttributeError('This object has no key \'search_uri\'')
