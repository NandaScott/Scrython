from .rulings_object import RulingsObject

class Mtgo(RulingsObject):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.url = 'cards/mtgo/{}/rulings'.format(self.id)
        super(Mtgo, self).__init__(self.url)
