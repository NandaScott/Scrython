from .rulings_object import RulingsObject

class Multiverse(RulingsObject):
    def __init__(self, **kwargs):
        self.id = str(kwargs.get('id'))
        self.url = 'cards/multiverse/{}/rulings'.format(self.id)
        super(Multiverse, self).__init__(self.url)
