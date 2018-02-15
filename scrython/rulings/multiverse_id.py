from .rulings_object import RulingsObject

class Multiverse(RulingsObject):
    def __init__(self, **kwargs):
        if kwargs.get('id') is None:
            raise TypeError('No id provided to search by')

        self.url = 'cards/multiverse/{}/rulings?'.format(str(kwargs.get('id')))
        super(Multiverse, self).__init__(self.url)
