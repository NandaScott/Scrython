from .rulings_object import RulingsObject

class Id(RulingsObject):
    """docstring for Id."""
    def __init__(self, _id):
        self.id = str(_id)
        self.url = 'cards/{}/rulings'.format(self.id)
        super(Id, self).__init__(self.url)
