from .scryfall_object import ScryfallObject


class RandomCard(ScryfallObject):
    """This will return a random card. No parameters are passed while creating."""
    def __init__(self):
        self.url = 'cards/random'
        super(RandomCard, self).__init__(self.url)
