from rulings_object import RulingsObject

class Multiverse(RulingsObject):
    """docstring for Multiverse."""
    def __init__(self, _id):
        self.id = str(_id)
        self.url = 'cards/multiverse/{}/rulings'.format(self.id)
        super(Multiverse, self).__init__(self.url)
