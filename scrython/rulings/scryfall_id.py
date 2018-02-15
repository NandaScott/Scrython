from .rulings_object import RulingsObject

class Id(RulingsObject):
    def __init__(self, **kwargs):
        if kwargs.get('id') is None:
            raise TypeError('No id provided to search by')

        self.url = 'cards/{}/rulings?'.format(str(kwargs.get('id')))
        super(Id, self).__init__(self.url)
