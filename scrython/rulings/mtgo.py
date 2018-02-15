from .rulings_object import RulingsObject

class Mtgo(RulingsObject):
    def __init__(self, **kwargs):
        if kwargs.get('id') is None:
            raise TypeError('No id provided to search by')

        self.url = 'cards/mtgo/{}/rulings?'.format(str(kwargs.get('id')))
        super(Mtgo, self).__init__(self.url)
