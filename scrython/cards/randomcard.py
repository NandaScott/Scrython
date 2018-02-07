from .cards_object import CardsObject


class Random(CardsObject):
    def __init__(self):
        self.url = 'cards/random'
        super(Random, self).__init__(self.url)
