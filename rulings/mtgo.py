from .rulings_object import RulingsObject

class Mtgo(RulingsObject):
    def __init__(self, _id):
        self.id = _id
        self.url = 'cards/mtgo/{}/rulings'.format(self.id)
        super(Mtgo, self).__init__(self.url)
